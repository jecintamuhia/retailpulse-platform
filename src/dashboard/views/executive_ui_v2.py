"""
RetailPulse Command Center — Alternative Design Concept v2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Design Philosophy: "Data Storytelling at a Glance"
- Narrative-driven layout: each section tells a story
- Hero metrics with embedded sparklines (trend context baked in)
- Insight callouts for pattern recognition
- Magazine-style grid with content hierarchy
- Period-over-period comparison baked into every metric
- Floating action bar for power-user workflows
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from ui_common import (
    render_kpi_card,
    render_section_header,
    render_page_heading,
    chart_theme,
    glass_panel_start,
    glass_panel_end,
    CHART_COLORS,
    icon,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    PRIMARY,
    SUCCESS,
    DANGER,
    WARNING,
    BG_SURFACE,
    BORDER,
    BORDER_ACTIVE,
    PRIMARY_GLOW,
    PRIMARY_LIGHT,
    BG_ELEVATED,
    BG_GLASS,
    SPACING,
)

DATA_PATH = "data/cleaned/transactions.csv"


# ── New Design System Extensions (v2) ───────────────────────────────────

V2_CSS = """
<style>
    .main .block-container {
        max-width: 1480px;
        padding-top: 1.25rem;
        padding-bottom: 3.5rem;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.85rem;
    }

    .stPlotlyChart {
        border-radius: 8px;
        overflow: hidden;
    }

    .glass-panel {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.055), rgba(255,255,255,0.02)),
            rgba(10, 13, 24, 0.62) !important;
        border: 1px solid rgba(255,255,255,0.075) !important;
        border-radius: 8px !important;
        box-shadow: 0 18px 45px rgba(0,0,0,0.22);
    }

    .rp-v2-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        padding: 18px 0 14px;
        margin-bottom: 4px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }

    .rp-v2-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
    }

    .rp-v2-logo {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        background:
            linear-gradient(135deg, rgba(16,185,129,0.95), rgba(20,184,166,0.85)),
            #10B981;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 28px rgba(16,185,129,0.28);
        flex: 0 0 auto;
    }

    .rp-v2-title {
        font-weight: 720;
        font-size: 1.45rem;
        color: #F8FAFC;
        line-height: 1.05;
    }

    .rp-v2-subtitle {
        font-size: 0.8rem;
        color: #7B8798;
        margin-top: 5px;
    }

    .rp-v2-actions {
        display: flex;
        gap: 8px;
        align-items: center;
        flex-wrap: wrap;
        justify-content: flex-end;
    }

    .rp-section-kicker {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 12px 0 16px;
    }

    .rp-section-kicker-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #7B8798;
        font-weight: 700;
        white-space: nowrap;
    }

    .rp-section-kicker-line {
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
    }

    .rp-section-kicker-note {
        font-size: 0.65rem;
        color: #697386;
        white-space: nowrap;
    }

    /* ── Hero Metric Cards ──────────────────── */
    .hero-metric {
        min-height: 128px;
        background:
            radial-gradient(circle at top right, rgba(16,185,129,0.12), transparent 38%),
            linear-gradient(145deg, rgba(18,22,35,0.94) 0%, rgba(12,15,26,0.78) 100%);
        border: 1px solid rgba(255,255,255,0.075);
        border-radius: 8px;
        padding: 18px 18px 14px;
        position: relative;
        overflow: hidden;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 14px 36px rgba(0,0,0,0.18);
    }
    .hero-metric::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10B981, #6366F1, #10B981);
        background-size: 200% 100%;
        animation: shimmerGradient 3s ease-in-out infinite;
    }
    @keyframes shimmerGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero-metric:hover {
        border-color: rgba(16,185,129,0.32);
        transform: translateY(-2px);
        box-shadow: 0 18px 48px rgba(0,0,0,0.28);
    }
    .hero-metric-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 8px;
    }
    .hero-metric-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #7B8798;
        font-weight: 700;
    }
    .hero-metric-value {
        font-size: clamp(1.5rem, 2vw, 2rem);
        font-weight: 700;
        color: #F1F5F9;
        line-height: 1.1;
        margin-bottom: 4px;
    }
    .hero-metric-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 600;
    }
    .hero-metric-badge.up { background: rgba(16,185,129,0.12); color: #10B981; }
    .hero-metric-badge.down { background: rgba(239,68,68,0.12); color: #EF4444; }
    .hero-metric .sparkline-wrap {
        margin-top: 10px;
        height: 32px;
        opacity: 0.6;
    }

    /* ── Insight Callout ────────────────────── */
    .insight-callout {
        background:
            linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(99,102,241,0.06) 100%),
            rgba(9,12,22,0.7);
        border: 1px solid rgba(16,185,129,0.18);
        border-radius: 8px;
        padding: 16px 18px;
        margin-bottom: 16px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
        animation: fadeInUp 0.5s ease;
        box-shadow: 0 16px 38px rgba(0,0,0,0.18);
    }
    .insight-callout-icon {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #10B981, #059669);
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-size: 0.85rem;
    }
    .insight-callout-text {
        color: #8892A4;
        font-size: 0.82rem;
        line-height: 1.5;
    }
    .insight-callout-text strong {
        color: #F1F5F9;
        font-weight: 600;
    }

    /* ── Data Story Section ─────────────────── */
    .data-story {
        margin: 4px 0 12px;
        animation: fadeInUp 0.5s ease;
    }
    .data-story-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 14px;
    }
    .data-story-title {
        font-size: 0.98rem;
        font-weight: 700;
        color: #F1F5F9;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .data-story-subtitle {
        font-size: 0.78rem;
        color: #5B6577;
        margin-top: 2px;
    }
    .data-story-badge {
        font-size: 0.65rem;
        padding: 4px 10px;
        border-radius: 999px;
        background: rgba(255,255,255,0.04);
        color: #A7B0BF;
        border: 1px solid rgba(255,255,255,0.06);
        white-space: nowrap;
    }

    /* ── Quick Stats Row ────────────────────── */
    .quick-stat {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.018));
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 8px;
        padding: 12px 14px;
        text-align: center;
        transition: all 0.2s ease;
        min-height: 72px;
    }
    .quick-stat:hover {
        background: rgba(255,255,255,0.04);
        border-color: rgba(255,255,255,0.08);
    }
    .quick-stat-value {
        font-size: 1.1rem;
        font-weight: 650;
        color: #F1F5F9;
    }
    .quick-stat-label {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #5B6577;
        font-weight: 600;
        margin-top: 2px;
    }

    /* ── Floating Action Bar ────────────────── */
    .action-bar {
        position: fixed;
        bottom: 24px;
        right: 24px;
        display: flex;
        gap: 8px;
        z-index: 999;
        animation: fadeInUp 0.6s ease;
    }
    .action-btn {
        width: 44px;
        height: 44px;
        border-radius: 8px;
        background: linear-gradient(135deg, #10B981, #059669);
        border: none;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.25s ease;
        box-shadow: 0 4px 16px rgba(16,185,129,0.25);
        font-size: 1.1rem;
    }
    .action-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(16,185,129,0.35);
    }
    .action-btn.secondary {
        background: #1A1D2E;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .action-btn.secondary:hover {
        background: #222640;
        border-color: rgba(255,255,255,0.12);
    }

    /* ── Chip Filter ────────────────────────── */
    .chip-filter-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 16px;
    }
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.03);
        color: #8892A4;
    }
    .chip:hover {
        border-color: rgba(255,255,255,0.12);
        background: rgba(255,255,255,0.06);
    }
    .chip.active {
        background: rgba(16,185,129,0.12);
        border-color: rgba(16,185,129,0.25);
        color: #10B981;
    }

    /* ── Comparison Pill ────────────────────── */
    .comparison-pill {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        background: rgba(16,185,129,0.1);
        color: #10B981;
    }
    .comparison-pill.negative {
        background: rgba(239,68,68,0.1);
        color: #EF4444;
    }

    section[data-testid="stSidebar"] {
        background: #090D16;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] .filter-label {
        color: #F1F5F9;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.075);
        border-radius: 8px;
        background: rgba(10,13,24,0.62);
        overflow: hidden;
    }

    div[data-testid="stExpander"] details summary {
        font-weight: 700;
        color: #F1F5F9;
    }

    @media (max-width: 900px) {
        .rp-v2-header {
            align-items: flex-start;
            flex-direction: column;
        }
        .rp-v2-actions {
            justify-content: flex-start;
        }
        .action-bar {
            right: 14px;
            bottom: 14px;
        }
    }

    /* Corporate blue and white presentation theme */
    .glass-panel {
        background: #FFFFFF !important;
        border: 1px solid rgba(30,64,175,0.12) !important;
        box-shadow: 0 18px 42px rgba(30,64,175,0.08) !important;
    }

    .rp-v2-header {
        border-bottom-color: rgba(30,64,175,0.12);
    }

    .rp-v2-logo,
    .insight-callout-icon,
    .action-btn {
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        box-shadow: 0 10px 28px rgba(37,99,235,0.22) !important;
    }

    .rp-v2-title,
    .hero-metric-value,
    .data-story-title,
    .quick-stat-value,
    div[data-testid="stExpander"] details summary {
        color: #0F172A !important;
    }

    .rp-v2-subtitle,
    .hero-metric-label,
    .data-story-subtitle,
    .quick-stat-label,
    .insight-callout-text {
        color: #64748B !important;
    }

    .hero-metric {
        background:
            radial-gradient(circle at top right, rgba(37,99,235,0.10), transparent 38%),
            linear-gradient(145deg, #FFFFFF 0%, #F8FBFF 100%) !important;
        border-color: rgba(30,64,175,0.14) !important;
        box-shadow: 0 18px 42px rgba(30,64,175,0.08) !important;
    }

    .hero-metric::after {
        background: linear-gradient(90deg, #2563EB, #60A5FA, #1D4ED8) !important;
    }

    .hero-metric:hover {
        border-color: rgba(37,99,235,0.34) !important;
        box-shadow: 0 22px 50px rgba(37,99,235,0.12) !important;
    }

    .hero-metric-badge.up,
    .comparison-pill,
    .chip.active {
        background: rgba(37,99,235,0.10) !important;
        border-color: rgba(37,99,235,0.20) !important;
        color: #1D4ED8 !important;
    }

    .insight-callout {
        background:
            linear-gradient(135deg, rgba(37,99,235,0.08), rgba(96,165,250,0.08)),
            #FFFFFF !important;
        border-color: rgba(37,99,235,0.16) !important;
        box-shadow: 0 18px 42px rgba(30,64,175,0.08) !important;
    }

    .insight-callout-text strong {
        color: #0F172A !important;
    }

    .data-story-badge,
    .quick-stat,
    .action-btn.secondary,
    div[data-testid="stExpander"] {
        background: #F8FBFF !important;
        border-color: rgba(30,64,175,0.12) !important;
        color: #475569 !important;
    }

    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right-color: rgba(30,64,175,0.12) !important;
    }
</style>
"""


def inject_v2_css():
    st.markdown(V2_CSS, unsafe_allow_html=True)


def _chart_layout(**overrides):
    """Merge chart_theme defaults with per-chart overrides without duplicate kwargs."""
    layout = chart_theme()
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(layout.get(key), dict):
            layout[key] = {**layout[key], **value}
        else:
            layout[key] = value
    return layout


# ── Helper: Build sparkline data from a series ──────────────────────────

def _sparkline_fig(values, color=PRIMARY, height=40):
    """Generate a minimal inline sparkline figure for hero metrics."""
    if values.empty or len(values) < 2:
        return None
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=values,
        mode="lines",
        line=dict(width=1.8, color=color),
        fill="tozeroy",
        fillcolor=f"rgba{tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.08,)}",
        showlegend=False,
        hoverinfo="skip",
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
    )
    return fig


def _delta_badge(current, previous):
    """Return HTML for a delta badge (positive/negative)."""
    if previous is None or previous == 0:
        return ""
    pct = ((current - previous) / previous) * 100
    cls = "up" if pct >= 0 else "down"
    arrow = "↑" if pct >= 0 else "↓"
    return f'<span class="hero-metric-badge {cls}">{arrow} {abs(pct):.1f}%</span>'


def _value_with_commas(x):
    if x >= 1_000_000:
        return f"${x/1_000_000:.1f}M"
    if x >= 1_000:
        return f"${x/1_000:.1f}K"
    return f"${x:,.0f}"


# ── Data Loading ────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    if "TotalPrice" not in df.columns:
        df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    return df


# ── Main Render Function ────────────────────────────────────────────────

def render_executive_ui_v2():
    inject_v2_css()

    # ── Data ──
    try:
        df = load_data()
    except FileNotFoundError:
        st.error(f"Dataset not found:\n\n{DATA_PATH}\n\nRun your data pipeline first.")
        return

    if df.empty:
        st.warning("Dataset is empty.")
        return

    # ── Sidebar: Quick Filters → inline chip style on main panel ──
    with st.sidebar:
        st.markdown('<div class="sidebar-filters"><div class="filter-label">Filters</div></div>', unsafe_allow_html=True)
        all_countries = sorted(df["Country"].dropna().unique())
        selected_countries = st.multiselect(
            "Country",
            options=all_countries,
            default=all_countries,
            key="v2_country_filter"
        )

    if selected_countries:
        df = df[df["Country"].isin(selected_countries)]

    if df.empty:
        st.warning("No data available for selected filters.")
        return

    # ── Compute Metrics ──
    total_revenue = df["TotalPrice"].sum()
    total_orders = df["InvoiceNo"].nunique()
    total_customers = df["CustomerID"].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    # Period-over-period (last month vs previous month)
    df["Month"] = df["InvoiceDate"].dt.month
    df["Year"] = df["InvoiceDate"].dt.year
    monthly_rev = df.groupby(["Year", "Month"])["TotalPrice"].sum().reset_index()
    if len(monthly_rev) >= 2:
        rev_cur = monthly_rev.iloc[-1]["TotalPrice"]
        rev_prev = monthly_rev.iloc[-2]["TotalPrice"]
    else:
        rev_cur = rev_prev = total_revenue

    orders_monthly = df.groupby(["Year", "Month"])["InvoiceNo"].nunique().reset_index()
    if len(orders_monthly) >= 2:
        ord_cur = orders_monthly.iloc[-1]["InvoiceNo"]
        ord_prev = orders_monthly.iloc[-2]["InvoiceNo"]
    else:
        ord_cur = ord_prev = total_orders

    # Daily series for sparklines
    daily_rev = df.groupby(df["InvoiceDate"].dt.date)["TotalPrice"].sum()
    daily_orders = df.groupby(df["InvoiceDate"].dt.date)["InvoiceNo"].nunique()

    # ──────────────────────────────────────────────────────────────────
    #  NEW LAYOUT: "Command Center" Magazine-Style
    # ──────────────────────────────────────────────────────────────────

    # ═══════════════════════════════════════════════════════════════════
    #  SECTION 1: PAGE HEADER + QUICK CONTROLS
    # ═══════════════════════════════════════════════════════════════════

    st.markdown("""
    <div class="rp-v2-header">
        <div class="rp-v2-brand">
            <div class="rp-v2-logo">
                <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" fill="white">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zM7 10h2v7H7v-7zm4-3h2v10h-2V7zm4 6h2v4h-2v-4z"/>
                </svg>
            </div>
            <div>
                <div class="rp-v2-title">Command Center</div>
                <div class="rp-v2-subtitle">Real-time retail pulse &bull; refreshed from the latest cleaned transactions</div>
            </div>
        </div>
        <div class="rp-v2-actions">
            <span class="data-story-badge">Last 30d</span>
            <span class="data-story-badge">MoM Comparison</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════
    #  SECTION 2: HERO METRICS ROW (with sparkline context)
    # ═══════════════════════════════════════════════════════════════════

    st.markdown("""
    <div class="rp-section-kicker">
        <span class="rp-section-kicker-label">Performance Overview</span>
        <span class="rp-section-kicker-line"></span>
        <span class="rp-section-kicker-note">30-day trend</span>
    </div>
    """, unsafe_allow_html=True)

    hero_cols = st.columns(4)

    metrics_data = [
        ("Revenue", _value_with_commas(total_revenue), "$", daily_rev, PRIMARY, rev_cur, rev_prev),
        ("Orders", f"{total_orders:,}", "#", daily_orders, "#0EA5E9", ord_cur, ord_prev),
        ("Customers", f"{total_customers:,}", "#", None, "#60A5FA", None, None),
        ("Avg Order Value", f"${avg_order_value:,.2f}", "$", None, "#1D4ED8", None, None),
    ]

    metric_colors = {
        "Revenue": PRIMARY,
        "Orders": "#0EA5E9",
        "Customers": "#60A5FA",
        "Avg Order Value": "#1D4ED8",
    }

    spark_rev = _sparkline_fig(daily_rev, color=PRIMARY, height=36)
    spark_ord = _sparkline_fig(daily_orders, color="#0EA5E9", height=36)

    spark_map = {
        "Revenue": spark_rev,
        "Orders": spark_ord,
    }

    for i, (label, value_str, prefix, series, color, cur, prev) in enumerate(metrics_data):
        with hero_cols[i]:
            # Delta
            delta_html = ""
            if cur is not None and prev is not None and prev > 0:
                pct = ((cur - prev) / prev) * 100
                cls = "up" if pct >= 0 else "down"
                arrow = "↑" if pct >= 0 else "↓"
                delta_html = f'<span class="hero-metric-badge {cls}">{arrow} {abs(pct):.1f}% vs prev. month</span>'

            st.markdown(f"""
            <div class="hero-metric" style="animation-delay:{i * 0.08}s;">
                <div class="hero-metric-top">
                    <span class="hero-metric-label">{label}</span>
                    <div style="display:flex; gap:4px; align-items:center; justify-content:flex-end;">
                        {delta_html}
                    </div>
                </div>
                <div class="hero-metric-value">{value_str}</div>
            </div>
            """, unsafe_allow_html=True)

    with hero_cols[0]:
        if spark_rev:
            st.plotly_chart(spark_rev, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("<div style='height:36px;'></div>", unsafe_allow_html=True)
    with hero_cols[1]:
        if spark_ord:
            st.plotly_chart(spark_ord, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("<div style='height:36px;'></div>", unsafe_allow_html=True)
    with hero_cols[2]:
        st.markdown("<div style='height:36px;'></div>", unsafe_allow_html=True)
    with hero_cols[3]:
        st.markdown("<div style='height:36px;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    
    if len(monthly_rev) >= 2:
        rev_trend = monthly_rev["TotalPrice"].pct_change().iloc[-1] * 100
        if rev_trend > 0:
            insight_text = f"Revenue grew <strong>{rev_trend:.1f}%</strong> month-over-month, driven by <strong>{df['Description'].value_counts().index[0] if not df.empty else 'top products'}</strong> — suggesting strong product-market alignment in current markets."
        else:
            insight_text = f"Revenue declined <strong>{abs(rev_trend):.1f}%</strong> month-over-month. Consider reviewing pricing strategy or running a promotional campaign in <strong>{df.groupby('Country')['TotalPrice'].sum().idxmax() if not df.empty else 'top markets'}</strong>."
    else:
        insight_text = "Data pipeline is active. <strong>View key metrics below</strong> to understand your current retail performance and identify growth opportunities."

    top_country = df.groupby("Country")["TotalPrice"].sum().idxmax() if not df.empty else "N/A"
    top_product = df.groupby("Description")["TotalPrice"].sum().idxmax() if not df.empty else "N/A"

    st.markdown(f"""
    <div class="insight-callout">
        <div class="insight-callout-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="white">
                <path d="M19 9l-1.5-1.5L19 6l1.5 1.5L19 9zm-6.5-2L11 5.5 13.5 4 16 5.5 13.5 7zM19 14l-1.5-1.5L19 11l1.5 1.5L19 14zM9 8L6.5 5.5 9 4l2.5 2.5L9 8zm5.5 2L13 8.5 15.5 6 18 8.5 15.5 10zM5 12l-1.5-1.5L5 9l1.5 1.5L5 12zm3 5l-2.5-2.5L8 12l2.5 2.5L8 17zm6-1l-2.5 2.5L9 16l2.5-2.5L14 16zm3-2l-1.5 1.5L14 14l1.5-1.5L17 14z"/>
            </svg>
        </div>
        <div class="insight-callout-text">
            <strong>AI Insight:</strong> {insight_text}
            &nbsp;&nbsp;·&nbsp;&nbsp;
            Top market: <strong>{top_country}</strong>
            &nbsp;&nbsp;·&nbsp;&nbsp;
            Top product: <strong>{top_product[:30]}{'…' if len(top_product) > 30 else ''}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

   
    col_left, col_right = st.columns([2, 1])

    with col_left:
       
        st.markdown("""
        <div class="data-story">
            <div class="data-story-header">
                <div>
                    <div class="data-story-title">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="#2563EB">
                            <path d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/>
                        </svg>
                        Revenue Growth Story
                    </div>
                    <div class="data-story-subtitle">Daily revenue trajectory with 7-day moving average</div>
                </div>
                <span class="data-story-badge">Daily · Trend</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        glass_panel_start()
        daily = df.groupby(df["InvoiceDate"].dt.date)["TotalPrice"].sum().reset_index()
        daily.columns = ["Date", "Revenue"]
        daily["MA7"] = daily["Revenue"].rolling(7).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily["Date"], y=daily["Revenue"],
            mode="lines+markers",
            name="Daily Revenue",
            line=dict(width=1.5, color=PRIMARY),
            marker=dict(size=3, color=PRIMARY, opacity=0.6),
            fill="tozeroy",
            fillcolor="rgba(37,99,235,0.08)",
        ))
        fig.add_trace(go.Scatter(
            x=daily["Date"], y=daily["MA7"],
            mode="lines",
            name="7-Day Avg",
            line=dict(width=2.5, color="#0EA5E9", dash="dot"),
        ))
        fig.update_layout(_chart_layout(
            height=380,
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1,
                font=dict(size=10, color=TEXT_SECONDARY),
            ),
            hovermode="x unified",
        ))
        st.plotly_chart(fig, use_container_width=True)
        glass_panel_end()

        st.markdown("""
        <div class="data-story">
            <div class="data-story-header">
                <div>
                    <div class="data-story-title">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="#6366F1">
                            <path d="M5 9.5h3v9H5v-9zm5.5-4h3v13h-3v-13zM16 12h3v6h-3v-6z"/>
                        </svg>
                        Monthly Revenue Breakdown
                    </div>
                    <div class="data-story-subtitle">Revenue distribution across months with YoY context</div>
                </div>
                <span class="data-story-badge">Monthly · Aggregated</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        glass_panel_start()
        monthly = df.groupby("Month")["TotalPrice"].sum().reset_index()
        monthly.columns = ["Month", "Revenue"]
        month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly["Month"].map(lambda m: month_labels[int(m)-1] if 1 <= int(m) <= 12 else m),
            y=monthly["Revenue"],
            marker=dict(
                color=monthly["Revenue"],
                colorscale=[
                    [0, "rgba(147,197,253,0.55)"],
                    [0.5, "rgba(96,165,250,0.78)"],
                    [1, "#2563EB"],
                ],
                showscale=False,
                line=dict(width=0),
            ),
            hovertemplate="%{x}<br>$%{y:,.0f}<extra></extra>",
        ))
        fig.update_layout(_chart_layout(
            height=320,
            showlegend=False,
            hovermode="x unified",
        ))
        fig.update_xaxes(tickangle=0)
        st.plotly_chart(fig, use_container_width=True)
        glass_panel_end()

    with col_right:
      
        st.markdown("""
        <div class="data-story">
            <div class="data-story-header">
                <div>
                    <div class="data-story-title" style="font-size:0.85rem;">
                        Quick Stats
                    </div>
                </div>
                <span class="data-story-badge">Snapshot</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        avg_daily = daily["Revenue"].mean() if not daily.empty else 0
        peak_day = daily.loc[daily["Revenue"].idxmax()] if not daily.empty else None
        peak_rev = peak_day["Revenue"] if peak_day is not None else 0
        peak_date = peak_day["Date"].strftime("%b %d") if peak_day is not None else "N/A"

        quick_stats = [
            ("Daily Avg", f"${avg_daily:,.0f}"),
            ("Peak Day", f"${peak_rev:,.0f}"),
            ("Peak Date", peak_date),
            ("Data Points", f"{len(df):,}"),
        ]

        stat_cols = st.columns(2)
        for idx, (label, value) in enumerate(quick_stats):
            with stat_cols[idx % 2]:
                st.markdown(f"""
                <div class="quick-stat" style="animation-delay:{idx * 0.05}s;">
                    <div class="quick-stat-value">{value}</div>
                    <div class="quick-stat-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="data-story">
            <div class="data-story-header">
                <div>
                    <div class="data-story-title" style="font-size:0.85rem;">
                        Top Products
                    </div>
                    <div class="data-story-subtitle">By revenue contribution</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        glass_panel_start()
        top_products = df.groupby("Description")["TotalPrice"].sum().nlargest(6).reset_index()
        fig = px.bar(
            top_products,
            y="Description",
            x="TotalPrice",
            orientation="h",
            color="TotalPrice",
            color_continuous_scale=["rgba(147,197,253,0.35)", "#2563EB"],
            template="plotly_white",
        )
        fig.update_traces(
            marker=dict(line=dict(width=0)),
            hovertemplate="%{y}<br>$%{x:,.0f}<extra></extra>",
        )
        fig.update_layout(_chart_layout(
            height=280,
            showlegend=False,
            xaxis_title=None,
            yaxis_title=None,
            margin=dict(l=0, r=0, t=8, b=0),
        ))
        fig.update_yaxes(autorange="reversed", tickfont=dict(size=9))
        st.plotly_chart(fig, use_container_width=True)
        glass_panel_end()
        st.markdown("""
        <div class="data-story">
            <div class="data-story-header">
                <div>
                    <div class="data-story-title" style="font-size:0.85rem;">
                        Market Distribution
                    </div>
                    <div class="data-story-subtitle">Revenue by country</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        glass_panel_start()
        country_rev = df.groupby("Country")["TotalPrice"].sum().nlargest(6).reset_index()
        fig = px.pie(
            country_rev,
            names="Country",
            values="TotalPrice",
            hole=0.6,
            color_discrete_sequence=CHART_COLORS,
            template="plotly_white",
        )
        fig.update_traces(
            textinfo="label+percent",
            textfont=dict(size=9, color=TEXT_SECONDARY),
            hovertemplate="%{label}<br>$%{value:,.0f} (%{percent})<extra></extra>",
        )
        fig.update_layout(_chart_layout(
            height=260,
            showlegend=False,
            margin=dict(l=0, r=0, t=8, b=0),
        ))
        st.plotly_chart(fig, use_container_width=True)
        glass_panel_end()

   
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    with st.expander("📋 Detailed Transaction View", expanded=False):
        st.dataframe(
            df[["InvoiceNo", "Description", "Quantity", "UnitPrice", "TotalPrice", "Country", "InvoiceDate"]]
            .sort_values("InvoiceDate", ascending=False)
            .head(100),
            use_container_width=True,
            height=300,
            column_config={
                "InvoiceDate": st.column_config.DatetimeColumn("Date", format="MMM DD, YY"),
                "TotalPrice": st.column_config.NumberColumn("Total", format="$%.2f"),
                "UnitPrice": st.column_config.NumberColumn("Unit Price", format="$%.2f"),
            }
        )

   
    st.markdown("""
    <div class="action-bar">
        <button class="action-btn secondary" title="Export Data" onclick="alert('Export ready')">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
            </svg>
        </button>
        <button class="action-btn" title="Refresh Dashboard" onclick="window.location.reload()">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
            </svg>
        </button>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_executive_ui_v2()
