import streamlit as st
import pandas as pd
import plotly.express as px

from ui_common import (
    render_kpi_card,
    render_section_header,
    render_page_heading,
    chart_theme,
    glass_panel_start,
    glass_panel_end,
    CHART_COLORS
)

DATA_PATH = "data/cleaned/transactions.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    if "TotalPrice" not in df.columns:
        df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    return df


def render_executive_ui():

    render_page_heading(
        "Executive Sales Dashboard",
        subtitle="Real-time revenue, order, and customer performance overview.",
        icon_name="monitoring"
    )

    try:
        df = load_data()
    except FileNotFoundError:
        st.error(f"Dataset not found:\n\n{DATA_PATH}\n\nRun your data pipeline first.")
        return

    if df.empty:
        st.warning("Dataset is empty.")
        return

    # ── Filters ──
    with st.sidebar:
        st.markdown('<div class="sidebar-filters"><div class="filter-label">Filters</div></div>', unsafe_allow_html=True)
        countries = st.multiselect(
            "Country",
            options=sorted(df["Country"].dropna().unique()),
            default=sorted(df["Country"].dropna().unique())
        )

    if countries:
        df = df[df["Country"].isin(countries)]

    if df.empty:
        st.warning("No data available for selected filters.")
        return

    # ── KPIs (staggered entrance animation) ──
    total_revenue = df["TotalPrice"].sum()
    total_orders = df["InvoiceNo"].nunique()
    total_customers = df["CustomerID"].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    cols = st.columns(4)
    with cols[0]:
        render_kpi_card("Revenue", f"${total_revenue:,.0f}", icon_name="payments", delay=0.0)
    with cols[1]:
        render_kpi_card("Orders", f"{total_orders:,}", icon_name="shopping_cart", delay=0.05)
    with cols[2]:
        render_kpi_card("Customers", f"{total_customers:,}", icon_name="group", delay=0.10)
    with cols[3]:
        render_kpi_card("Avg Order", f"${avg_order_value:,.2f}", icon_name="receipt_long", delay=0.15)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        # ── Revenue Trend ──
        glass_panel_start()
        render_section_header("Revenue Trend", icon_name="trending_up")
        daily = df.groupby(df["InvoiceDate"].dt.date)["TotalPrice"].sum().reset_index()
        daily.columns = ["Date", "Revenue"]
        fig = px.line(
            daily, x="Date", y="Revenue",
            color_discrete_sequence=[CHART_COLORS[0]],
            template="plotly_white"
        )
        fig.update_traces(line=dict(width=2.5), fill="tozeroy", fillcolor="rgba(16,185,129,0.05)")
        fig.update_layout(height=350, showlegend=False, **chart_theme())
        st.plotly_chart(fig, width='stretch')
        glass_panel_end()

        # ── Monthly Performance ──
        glass_panel_start()
        render_section_header("Monthly Performance", icon_name="bar_chart")
        monthly = df.groupby(df["InvoiceDate"].dt.month)["TotalPrice"].sum().reset_index()
        monthly.columns = ["Month", "Revenue"]
        fig = px.bar(
            monthly, x="Month", y="Revenue",
            color_discrete_sequence=[CHART_COLORS[0]],
            template="plotly_white"
        )
        fig.update_traces(
            marker=dict(line=dict(width=0)),
            hovertemplate="Month %{x}<br>$%{y:,.0f}<extra></extra>"
        )
        fig.update_layout(height=300, showlegend=False, **chart_theme())
        fig.update_xaxes(tickmode="array", tickvals=list(range(1, 13)))
        st.plotly_chart(fig, width='stretch')
        glass_panel_end()

    with col_right:
        # ── Product Share ──
        glass_panel_start()
        render_section_header("Product Share", icon_name="pie_chart")
        product_rev = df.groupby("Description")["TotalPrice"].sum().nlargest(5).reset_index()
        fig = px.pie(
            product_rev, names="Description", values="TotalPrice",
            hole=0.55, color_discrete_sequence=CHART_COLORS,
            template="plotly_white"
        )
        fig.update_traces(textinfo="label+percent", textfont=dict(size=9))
        fig.update_layout(height=300, showlegend=False, **chart_theme())
        st.plotly_chart(fig, width='stretch')
        glass_panel_end()

        # ── Top Countries ──
        glass_panel_start()
        render_section_header("Top Countries", icon_name="public")
        country_rev = df.groupby("Country")["TotalPrice"].sum().nlargest(8).reset_index()
        fig = px.bar(
            country_rev, x="Country", y="TotalPrice",
            color="Country", color_discrete_sequence=CHART_COLORS,
            template="plotly_white"
        )
        fig.update_traces(
            marker=dict(line=dict(width=0)),
            hovertemplate="%{x}<br>$%{y:,.0f}<extra></extra>"
        )
        fig.update_layout(
            height=350, showlegend=False,
            xaxis_title=None, yaxis_title=None,
            **chart_theme()
        )
        st.plotly_chart(fig, width='stretch')
        glass_panel_end()


if __name__ == "__main__":
    render_executive_ui()
