import pickle

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ui_common import (
    CHART_COLORS,
    DANGER,
    PRIMARY,
    SUCCESS,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WARNING,
    chart_theme,
    glass_panel_end,
    glass_panel_start,
    icon,
    render_kpi_card,
    render_page_heading,
    render_section_header,
)

RFM_PATH = "data/features/rfm.csv"
MODEL_PATH = "data/models/churn_model.pkl"
FEATURE_COLS = [
    "Recency",
    "Frequency",
    "Monetary",
    "avg_order_value",
    "total_items",
    "unique_products",
]


CHURN_CSS = """
<style>
    .churn-command-strip {
        display: grid;
        grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.6fr);
        gap: 16px;
        margin: 6px 0 18px;
    }

    .churn-insight-panel {
        min-height: 124px;
        border-radius: 8px;
        border: 1px solid rgba(239,68,68,0.16);
        background:
            radial-gradient(circle at top left, rgba(239,68,68,0.13), transparent 32%),
            linear-gradient(135deg, rgba(17,19,30,0.92), rgba(10,13,24,0.72));
        padding: 18px 20px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.22);
    }

    .churn-insight-label {
        color: #FCA5A5;
        font-size: 0.68rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 750;
        margin-bottom: 10px;
    }

    .churn-insight-copy {
        color: #A7B0BF;
        line-height: 1.55;
        font-size: 0.9rem;
    }

    .churn-insight-copy strong {
        color: #F8FAFC;
        font-weight: 750;
    }

    .churn-action-card {
        min-height: 124px;
        border-radius: 8px;
        border: 1px solid rgba(16,185,129,0.16);
        background:
            radial-gradient(circle at top right, rgba(16,185,129,0.12), transparent 38%),
            rgba(10,13,24,0.72);
        padding: 18px 20px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.18);
    }

    .churn-action-title {
        color: #F8FAFC;
        font-size: 1rem;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .churn-action-meta {
        color: #7B8798;
        font-size: 0.78rem;
        line-height: 1.45;
    }

    .risk-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 750;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .risk-critical { background: rgba(239,68,68,0.13); color: #FCA5A5; border: 1px solid rgba(239,68,68,0.22); }
    .risk-watch { background: rgba(245,158,11,0.13); color: #FCD34D; border: 1px solid rgba(245,158,11,0.22); }
    .risk-stable { background: rgba(16,185,129,0.12); color: #6EE7B7; border: 1px solid rgba(16,185,129,0.2); }

    @media (max-width: 900px) {
        .churn-command-strip {
            grid-template-columns: 1fr;
        }
    }
</style>
"""


def _chart_layout(**overrides):
    layout = chart_theme()
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(layout.get(key), dict):
            layout[key] = {**layout[key], **value}
        else:
            layout[key] = value
    return layout


@st.cache_data
def load_rfm():
    return pd.read_csv(RFM_PATH)


@st.cache_resource
def load_churn_model():
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except Exception:
        return None


def _scale_series(series, invert=False):
    low = series.quantile(0.02)
    high = series.quantile(0.98)
    scaled = ((series.clip(low, high) - low) / (high - low)) if high > low else series * 0
    scaled = scaled.clip(0, 1)
    return 1 - scaled if invert else scaled


def _heuristic_risk(df):
    recency = _scale_series(df["Recency"])
    frequency = _scale_series(df["Frequency"], invert=True)
    monetary = _scale_series(df["Monetary"], invert=True)
    breadth = _scale_series(df["unique_products"], invert=True)
    risk = (0.48 * recency) + (0.24 * frequency) + (0.18 * monetary) + (0.10 * breadth)
    return risk.clip(0, 1)


def _score_customers(rfm):
    scored = rfm.copy()
    model = load_churn_model()
    source = "Model"
    heuristic = _heuristic_risk(scored)

    try:
        if model is not None and hasattr(model, "predict_proba"):
            model_scores = pd.Series(model.predict_proba(scored[FEATURE_COLS])[:, 1], index=scored.index)
            if model_scores.round(4).nunique() <= 3:
                scored["risk_score"] = ((0.55 * model_scores) + (0.45 * heuristic)).clip(0, 1)
                source = "Model + RFM calibration"
            else:
                scored["risk_score"] = model_scores
        else:
            source = "Heuristic"
            scored["risk_score"] = heuristic
    except Exception:
        source = "Heuristic"
        scored["risk_score"] = heuristic

    scored["risk_band"] = pd.cut(
        scored["risk_score"],
        bins=[-0.01, 0.35, 0.75, 1.01],
        labels=["Stable", "Watch", "Critical"],
    )
    scored["retention_value"] = scored["risk_score"] * scored["Monetary"]
    scored["next_best_action"] = scored.apply(_next_best_action, axis=1)
    return scored, source, model


def _next_best_action(row):
    if row["risk_score"] >= 0.65 and row["Monetary"] >= 1000:
        return "Executive win-back offer"
    if row["risk_score"] >= 0.65:
        return "Urgent reactivation email"
    if row["risk_score"] >= 0.35 and row["Frequency"] <= 2:
        return "Second-purchase incentive"
    if row["risk_score"] >= 0.35:
        return "Personalized replenishment"
    return "Maintain loyalty cadence"


def _feature_importance(model):
    labels = {
        "Recency": "Recency",
        "Frequency": "Frequency",
        "Monetary": "Spend",
        "avg_order_value": "Avg order value",
        "total_items": "Items",
        "unique_products": "Product breadth",
    }
    if model is not None and hasattr(model, "feature_importances_"):
        values = model.feature_importances_
    else:
        values = [0.48, 0.24, 0.18, 0.04, 0.02, 0.10]

    importance = pd.DataFrame({
        "Driver": [labels[col] for col in FEATURE_COLS],
        "Importance": values,
    })
    return importance.sort_values("Importance", ascending=True)


def _risk_pill(label):
    cls = {
        "Critical": "risk-critical",
        "Watch": "risk-watch",
        "Stable": "risk-stable",
    }.get(str(label), "risk-stable")
    return f'<span class="risk-pill {cls}">{label}</span>'


def render_churn_ui():
    st.markdown(CHURN_CSS, unsafe_allow_html=True)
    render_page_heading(
        "Churn Prediction",
        subtitle="Prioritize at-risk customers, understand churn drivers, and plan retention plays.",
        icon_name="insights",
    )

    try:
        rfm = load_rfm()
    except FileNotFoundError:
        st.error(f"RFM feature table not found: {RFM_PATH}")
        return

    missing = [col for col in FEATURE_COLS + ["is_churned"] if col not in rfm.columns]
    if missing:
        st.error(f"RFM table is missing required columns: {', '.join(missing)}")
        return

    scored, scoring_source, model = _score_customers(rfm)
    total_customers = len(scored)
    critical = int((scored["risk_band"] == "Critical").sum())
    watch = int((scored["risk_band"] == "Watch").sum())
    avg_risk = scored["risk_score"].mean()
    revenue_at_risk = scored.loc[scored["risk_band"] == "Critical", "Monetary"].sum()

    cols = st.columns(4)
    with cols[0]:
        render_kpi_card("Customers Scored", f"{total_customers:,}", icon_name="group")
    with cols[1]:
        render_kpi_card("Critical Risk", f"{critical:,}", icon_name="bolt", delta=-(critical / total_customers * 100) if total_customers else 0)
    with cols[2]:
        render_kpi_card("Watch List", f"{watch:,}", icon_name="trackpad_target")
    with cols[3]:
        render_kpi_card("Revenue at Risk", f"${revenue_at_risk:,.0f}", icon_name="payments")

    top_queue = scored.sort_values("retention_value", ascending=False).head(1)
    top_customer = int(top_queue.iloc[0]["CustomerID"]) if not top_queue.empty else "N/A"
    top_action = top_queue.iloc[0]["next_best_action"] if not top_queue.empty else "No action"
    actual_churn_rate = scored["is_churned"].mean() * 100

    st.markdown(f"""
    <div class="churn-command-strip">
        <div class="churn-insight-panel">
            <div class="churn-insight-label">Retention Brief</div>
            <div class="churn-insight-copy">
                <strong>{critical:,}</strong> customers are in the critical-risk band and represent
                <strong>${revenue_at_risk:,.0f}</strong> in historic value. The observed churn label rate in
                this feature set is <strong>{actual_churn_rate:.1f}%</strong>, with scoring powered by
                <strong>{scoring_source}</strong>.
            </div>
        </div>
        <div class="churn-action-card">
            <div class="churn-action-title">{icon("verified", size=16, color=PRIMARY)} Next Best Action</div>
            <div class="churn-action-meta">
                Prioritize customer <strong style="color:{TEXT_PRIMARY};">{top_customer}</strong> for
                <strong style="color:{TEXT_PRIMARY};">{top_action}</strong>. Sort the retention queue below by
                value to work the most material accounts first.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.25, 0.75])

    with left:
        glass_panel_start()
        render_section_header("Risk Landscape", icon_name="trackpad_target")
        fig = px.scatter(
            scored,
            x="Recency",
            y="Monetary",
            color="risk_band",
            size="risk_score",
            size_max=18,
            color_discrete_map={
                "Stable": SUCCESS,
                "Watch": WARNING,
                "Critical": DANGER,
            },
            hover_data={
                "CustomerID": True,
                "Frequency": True,
                "risk_score": ":.1%",
                "retention_value": ":,.0f",
            },
            template="plotly_dark",
        )
        fig.update_layout(_chart_layout(
            height=410,
            xaxis_title="Days Since Last Purchase",
            yaxis_title="Customer Monetary Value",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        ))
        fig.update_traces(marker=dict(line=dict(width=0.5, color="rgba(255,255,255,0.18)"), opacity=0.78))
        st.plotly_chart(fig, use_container_width=True)
        glass_panel_end()

    with right:
        glass_panel_start()
        render_section_header("Risk Mix", icon_name="pie_chart")
        risk_counts = scored["risk_band"].value_counts().rename_axis("Risk").reset_index(name="Customers")
        fig = px.pie(
            risk_counts,
            names="Risk",
            values="Customers",
            hole=0.62,
            color="Risk",
            color_discrete_map={
                "Stable": SUCCESS,
                "Watch": WARNING,
                "Critical": DANGER,
            },
        )
        fig.update_traces(textinfo="label+percent", textfont=dict(size=11, color=TEXT_SECONDARY))
        fig.update_layout(_chart_layout(height=410, showlegend=False, margin=dict(l=0, r=0, t=10, b=0)))
        st.plotly_chart(fig, use_container_width=True)
        glass_panel_end()

    lower_left, lower_right = st.columns([0.85, 1.15])

    with lower_left:
        glass_panel_start()
        render_section_header("Primary Churn Drivers", icon_name="bar_chart")
        importance = _feature_importance(model)
        fig = px.bar(
            importance,
            x="Importance",
            y="Driver",
            orientation="h",
            color="Importance",
            color_continuous_scale=["rgba(16,185,129,0.22)", "#10B981"],
            template="plotly_dark",
        )
        fig.update_traces(hovertemplate="%{y}<br>%{x:.3f}<extra></extra>", marker=dict(line=dict(width=0)))
        fig.update_layout(_chart_layout(
            height=350,
            showlegend=False,
            xaxis_title=None,
            yaxis_title=None,
            margin=dict(l=0, r=0, t=8, b=0),
        ))
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        glass_panel_end()

    with lower_right:
        glass_panel_start()
        render_section_header("Retention Queue", icon_name="receipt_long")
        queue = scored.sort_values("retention_value", ascending=False).head(25).copy()
        queue["Risk"] = queue["risk_band"].astype(str)
        queue["Risk Score"] = queue["risk_score"] * 100
        queue["Customer"] = queue["CustomerID"].astype(int).astype(str)
        queue["Historic Value"] = queue["Monetary"]
        queue["Action"] = queue["next_best_action"]

        st.dataframe(
            queue[["Customer", "Risk", "Risk Score", "Recency", "Frequency", "Historic Value", "Action"]],
            use_container_width=True,
            height=350,
            column_config={
                "Risk Score": st.column_config.ProgressColumn("Risk Score", format="%.0f%%", min_value=0, max_value=100),
                "Historic Value": st.column_config.NumberColumn("Historic Value", format="$%.0f"),
                "Recency": st.column_config.NumberColumn("Recency", help="Days since last purchase"),
            },
            hide_index=True,
        )
        glass_panel_end()

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    with st.expander("Customer lookup", expanded=False):
        customer_ids = scored["CustomerID"].astype(int).sort_values().tolist()
        selected_customer = st.selectbox("Customer", customer_ids, index=0)
        customer = scored[scored["CustomerID"].astype(int) == selected_customer].iloc[0]
        c1, c2, c3 = st.columns([0.7, 1, 1])
        with c1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=float(customer["risk_score"] * 100),
                number={"suffix": "%", "font": {"color": TEXT_PRIMARY}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": TEXT_MUTED},
                    "bar": {"color": DANGER if customer["risk_score"] >= 0.65 else WARNING if customer["risk_score"] >= 0.35 else SUCCESS},
                    "bgcolor": "rgba(255,255,255,0.03)",
                    "bordercolor": "rgba(255,255,255,0.08)",
                    "steps": [
                        {"range": [0, 35], "color": "rgba(16,185,129,0.13)"},
                        {"range": [35, 65], "color": "rgba(245,158,11,0.13)"},
                        {"range": [65, 100], "color": "rgba(239,68,68,0.13)"},
                    ],
                },
            ))
            fig.update_layout(_chart_layout(height=220, margin=dict(l=12, r=12, t=12, b=12)))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown(
                f"""
                <div class="churn-action-card">
                    <div class="churn-action-title">Customer {int(customer["CustomerID"])}</div>
                    <div class="churn-action-meta">
                        {_risk_pill(customer["risk_band"])}
                        <br><br>
                        Recency: <strong style="color:{TEXT_PRIMARY};">{customer["Recency"]:.0f} days</strong><br>
                        Frequency: <strong style="color:{TEXT_PRIMARY};">{customer["Frequency"]:.0f} orders</strong><br>
                        Value: <strong style="color:{TEXT_PRIMARY};">${customer["Monetary"]:,.0f}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f"""
                <div class="churn-action-card">
                    <div class="churn-action-title">Recommended Play</div>
                    <div class="churn-action-meta">
                        <strong style="color:{TEXT_PRIMARY};">{customer["next_best_action"]}</strong>
                        <br><br>
                        Product breadth: <strong style="color:{TEXT_PRIMARY};">{customer["unique_products"]:.0f}</strong><br>
                        Avg order value: <strong style="color:{TEXT_PRIMARY};">${customer["avg_order_value"]:,.0f}</strong><br>
                        Labeled churn: <strong style="color:{TEXT_PRIMARY};">{'Yes' if customer["is_churned"] else 'No'}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
