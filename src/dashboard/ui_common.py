

import streamlit as st

PRIMARY = "#2563EB"       
PRIMARY_GLOW = "rgba(37, 99, 235, 0.18)"
PRIMARY_LIGHT = "rgba(37, 99, 235, 0.08)"
PRIMARY_DARK = "#1D4ED8"
PRIMARY_GRADIENT = "linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)"

BG_APP = "#F7FAFF"
BG_SURFACE = "#FFFFFF"
BG_SURFACE_HOVER = "#F1F5FF"
BG_ELEVATED = "#EEF4FF"
BG_GLASS = "rgba(255, 255, 255, 0.86)"

BORDER = "rgba(30, 64, 175, 0.12)"
BORDER_HOVER = "rgba(30, 64, 175, 0.20)"
BORDER_ACTIVE = "rgba(37, 99, 235, 0.36)"

TEXT_PRIMARY = "#0F172A"
TEXT_SECONDARY = "#475569"
TEXT_MUTED = "#64748B"
TEXT_BRAND = "#2563EB"

SUCCESS = "#0EA5E9"
WARNING = "#F59E0B"
DANGER = "#EF4444"
INFO = "#3B82F6"

# ── Rich Chart Color Palette ────────────────────────────────────────────────
CHART_COLORS = [
    "#2563EB",  # blue
    "#0EA5E9",  # sky
    "#1D4ED8",  # royal blue
    "#60A5FA",  # light blue
    "#0369A1",  # deep sky
    "#93C5FD",  # pale blue
    "#64748B",  # slate
    "#F59E0B",  # amber accent
]

CHART_COLOR_CYCLE = ",".join(CHART_COLORS)

# ── Spacing Scale ─────────────────────────────────────────────────────────
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
}

# ── Inline SVG Icons (no external dependencies) ──────────────────────────
_ICON_PATHS = {
    "auto_awesome": "M19 9l-1.5-1.5L19 6l1.5 1.5L19 9zm-6.5-2L11 5.5 13.5 4 16 5.5 13.5 7zM19 14l-1.5-1.5L19 11l1.5 1.5L19 14zM9 8L6.5 5.5 9 4l2.5 2.5L9 8zm5.5 2L13 8.5 15.5 6 18 8.5 15.5 10zM5 12l-1.5-1.5L5 9l1.5 1.5L5 12zm3 5l-2.5-2.5L8 12l2.5 2.5L8 17zm6-1l-2.5 2.5L9 16l2.5-2.5L14 16zm3-2l-1.5 1.5L14 14l1.5-1.5L17 14z",
    "auto_graph": "M14.06 9.94L12 9l2.06-.94L15 6l.94 2.06L18 9l-2.06.94L15 12l-.94-2.06zM4 14l2.06-.94L7 11l.94 2.06L10 14l-2.06.94L7 17l-.94-2.06L4 14zm4.5-5l2.06-.94L11.5 6l.94 2.06L14.5 9l-2.06.94L11.5 12l-.94-2.06L8.5 9z",
    "bar_chart": "M5 9.5h3v9H5v-9zm5.5-4h3v13h-3v-13zM16 12h3v6h-3v-6z",
    "calendar_month": "M19 3h-1V1h-2v2H8V1H6v2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h2v2H7v-2zm4 0h2v2h-2v-2zm4 0h2v2h-2v-2z",
    "diamond": "M12 2L3 9l4 12h10l4-12-9-7zm0 3.73L17.2 9H6.8L12 5.73zM13 20h-2v-9h2v9z",
    "diversity_3": "M6.5 5.5C5.67 5.5 5 4.83 5 4s.67-1.5 1.5-1.5S8 3.17 8 4s-.67 1.5-1.5 1.5zM4 11c0-1.1.9-2 2-2h1c1.1 0 2 .9 2 2v5h-.5v3h-4v-3H4v-5zm12-5.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5S17.5 3.17 17.5 4s-.67 1.5-1.5 1.5zM16 9c1.1 0 2 .9 2 2v5h-1.5v3h-4v-3H12v-5c0-1.1.9-2 2-2h2zm-4 0c1.1 0 2 .9 2 2v2h-2v4h-2v-4H8v-2c0-1.1.9-2 2-2h2z",
    "group": "M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z",
    "link": "M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z",
    "monitoring": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zM7 10h2v7H7v-7zm4-3h2v10h-2V7zm4 6h2v4h-2v-4z",
    "payments": "M19 14V6c0-1.1-.9-2-2-2H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zm-2 0H3V6h14v8zm-7-4c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3zm13-4v11c0 1.1-.9 2-2 2H4v-2h17V7h2z",
    "pie_chart": "M11 2v20c-5.07-.5-9-4.79-9-10s3.93-9.5 9-10zm2 0v9h9c-.5-4.74-4.26-8.5-9-9zm0 11v9c4.74-.5 8.5-4.26 9-9h-9z",
    "public": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z",
    "receipt_long": "M19.5 3.5L18 2l-1.5 1.5L15 2l-1.5 1.5L12 2l-1.5 1.5L9 2 7.5 3.5 6 2 4.5 3.5 3 2v20l1.5-1.5L6 22l1.5-1.5L9 22l1.5-1.5L12 22l1.5-1.5L15 22l1.5-1.5L18 22l1.5-1.5L21 22V2l-1.5 1.5zM19 19.09H5V4.91h14v14.18zM6 15h12v2H6v-2zm0-4h12v2H6v-2zm0-4h12v2H6V7z",
    "schedule": "M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z",
    "shopping_cart": "M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zm10 0c-1.1 0-1.99.9-1.99 2S15.9 22 17 22s2-.9 2-2-.9-2-2-2zM7.17 14.75l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.86-7.01L19.42 4h-.01l-1.1 2H8.53L8.38 5H5.21l-.94-2H1.17v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25z",
    "star": "M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z",
    "trackpad_target": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm4-8c0 2.21-1.79 4-4 4s-4-1.79-4-4 1.79-4 4-4 4 1.79 4 4zm-2 0c0-1.1-.9-2-2-2s-2 .9-2 2 .9 2 2 2 2-.9 2-2z",
    "trending_up": "M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z",
    "bolt": "M11 21h-1l1-7H7.5c-.88 0-.33-.75-.31-.78C8.48 10.94 10.42 7.54 13.01 3h1l-1 7h3.51c.4 0 .62.19.4.66C12.97 17.55 11 21 11 21z",
    "insights": "M21 8c-1.45 0-2.26 1.44-1.93 2.51l-3.6 3.6c-.34-.07-.69-.11-1.05-.11s-.71.04-1.05.11l-2.6-2.6c.31-.98-.1-2.1-1.1-2.51-.9-.37-1.91-.06-2.45.59l-4.1 4.1c-.27.27-.27.71 0 .98.27.27.71.27.98 0l4.1-4.1c.31-.31.85-.27 1.05.07l2.6 2.6c-.3.97.05 2.08 1.02 2.57.97.5 2.14.17 2.71-.74l3.6-3.6c.38.12.78.18 1.18.18 1.66 0 3-1.34 3-3s-1.34-3-3-3z",
    "verified": "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z",
}

_DEFAULT_ICON = "bar_chart"


def icon(name, size=18, color=None):
    """
    Render an inline SVG icon (Material Design style).
    No external font dependencies needed.
    """
    c = color or TEXT_SECONDARY
    path = _ICON_PATHS.get(name, _ICON_PATHS.get(_DEFAULT_ICON, ""))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'style="vertical-align:middle; line-height:1; display:inline-block; flex-shrink:0;">'
        f'<path d="{path}" fill="{c}" /></svg>'
    )


# ── Global CSS ────────────────────────────────────────────────────────────

GLOBAL_CSS = f"""
<style>
    /* ── Keyframes ──────────────────────────── */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to   {{ opacity: 1; }}
    }}
    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 0 8px rgba(16,185,129,0.2); }}
        50%  {{ box-shadow: 0 0 18px rgba(16,185,129,0.5); }}
    }}
    @keyframes slideInRight {{
        from {{ opacity: 0; transform: translateX(-10px); }}
        to   {{ opacity: 1; transform: translateX(0); }}
    }}
    @keyframes shimmer {{
        0%   {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    @keyframes scaleIn {{
        from {{ opacity: 0; transform: scale(0.95); }}
        to   {{ opacity: 1; transform: scale(1); }}
    }}

    /* ── Base ───────────────────────────────── */
    .stApp {{
        background: {BG_APP} !important;
    }}
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }}
    .stApp > header {{
        display: none !important;
    }}
    #root > div:first-child > div:first-child > div:first-child > div:first-child {{
        padding-top: 0 !important;
    }}
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        animation: fadeIn 0.4s ease;
    }}
    .main > div {{
        animation: fadeInUp 0.5s ease;
    }}

    /* ── Typography ─────────────────────────── */
    h1, h2, h3, h4, h5, h6 {{
        letter-spacing: -0.02em;
    }}

    /* ── Sidebar ────────────────────────────── */
    [data-testid="stSidebar"] {{
        background: {BG_SURFACE} !important;
        border-right: 1px solid {BORDER} !important;
        padding-top: 0 !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 0 !important;
    }}

    /* Sidebar navigation cards */
    .nav-card {{
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 2px 0;
        background: transparent;
        border: 1px solid transparent;
        position: relative;
        animation: slideInRight 0.4s ease backwards;
    }}
    .nav-card:hover {{
        background: {BG_SURFACE_HOVER} !important;
        border-color: {BORDER} !important;
    }}
    .nav-card.active {{
        background: {PRIMARY_LIGHT} !important;
        border-color: {BORDER_ACTIVE} !important;
    }}
    .nav-card.active::before {{
        content: '';
        position: absolute;
        left: -1px;
        top: 50%;
        transform: translateY(-50%);
        width: 3px;
        height: 18px;
        background: {PRIMARY};
        border-radius: 0 3px 3px 0;
        box-shadow: 0 0 8px rgba(16,185,129,0.4);
    }}
    .nav-card .nav-icon {{
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-size: 0.85rem;
        transition: all 0.2s ease;
    }}
    .nav-card.active .nav-icon {{
        background: {PRIMARY_GRADIENT} !important;
    }}
    .nav-card:not(.active) .nav-icon {{
        background: rgba(255,255,255,0.04) !important;
    }}
    .nav-card .nav-label {{
        font-size: 0.85rem;
        font-weight: 500;
        color: {TEXT_SECONDARY};
        transition: color 0.2s;
        line-height: 1.2;
    }}
    .nav-card.active .nav-label {{
        color: {TEXT_PRIMARY};
    }}
    .nav-card:hover .nav-label {{
        color: {TEXT_PRIMARY};
    }}
    .nav-card .nav-sub {{
        font-size: 0.65rem;
        color: {TEXT_MUTED};
        margin-top: 1px;
    }}

    /* Sidebar extra elements */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: {TEXT_PRIMARY} !important;
    }}

    /* Sidebar filters section */
    .sidebar-filters {{
        padding: 12px 0;
        margin-top: 8px;
        border-top: 1px solid {BORDER};
    }}
    .sidebar-filters .filter-label {{
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {TEXT_MUTED};
        font-weight: 600;
        margin-bottom: 10px;
    }}

    /* ── Buttons ────────────────────────────── */
    .stButton > button {{
        background: {PRIMARY_GRADIENT} !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 7px 20px !important;
        font-weight: 500 !important;
        font-size: 0.825rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(16,185,129,0.15) !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(16,185,129,0.3) !important;
    }}
    .stButton > button:active {{
        transform: translateY(0) !important;
    }}

    /* ── Select / Multiselect ──────────────── */
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {{
        background: {BG_ELEVATED} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
        color: {TEXT_PRIMARY} !important;
        transition: border-color 0.2s !important;
    }}
    .stSelectbox div[data-baseweb="select"] > div:hover,
    .stMultiSelect div[data-baseweb="select"] > div:hover {{
        border-color: {BORDER_HOVER} !important;
    }}

    /* ── Tabs ───────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
        padding: 3px;
        border: none;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 7px !important;
        padding: 6px 16px !important;
        font-weight: 450;
        font-size: 0.8rem;
        color: {TEXT_MUTED} !important;
        transition: all 0.2s ease !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: {TEXT_SECONDARY} !important;
        background: rgba(255,255,255,0.03) !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {BG_SURFACE} !important;
        color: {TEXT_PRIMARY} !important;
    }}

    /* ── DataFrames ─────────────────────────── */
    .stDataFrame {{
        border-radius: 12px !important;
        overflow: hidden;
        border: 1px solid {BORDER} !important;
    }}

    /* ── Glass Panel / Card ────────────────── */
    .glass-panel {{
        background: {BG_SURFACE} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 14px !important;
        padding: 22px !important;
        margin-bottom: 18px;
        transition: all 0.25s ease;
        animation: scaleIn 0.35s ease backwards;
    }}
    .glass-panel:hover {{
        border-color: {BORDER_ACTIVE} !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
    }}

    /* ── KPI Cards ──────────────────────────── */
    .kpi-card {{
        background: {BG_SURFACE};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 18px 16px 16px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.5s ease backwards;
    }}
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: {PRIMARY_GRADIENT};
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    .kpi-card:hover {{
        border-color: {BORDER_ACTIVE};
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(16,185,129,0.08);
    }}
    .kpi-card:hover::before {{
        opacity: 1;
    }}
    .kpi-card .kpi-icon-wrap {{
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: {PRIMARY_LIGHT};
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 8px;
        transition: all 0.3s ease;
    }}
    .kpi-card:hover .kpi-icon-wrap {{
        background: {PRIMARY_GLOW};
        transform: scale(1.05);
    }}
    .kpi-title {{
        color: {TEXT_MUTED};
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-bottom: 6px;
    }}
    .kpi-value {{
        color: {TEXT_PRIMARY};
        font-size: 1.65rem;
        font-weight: 650;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }}

    /* ── Section Header ─────────────────────── */
    .section-header {{
        font-size: 0.85rem;
        font-weight: 550;
        color: {TEXT_PRIMARY};
        margin-bottom: 14px;
        padding-bottom: 10px;
        border-bottom: 1px solid {BORDER};
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: -0.01em;
    }}

    /* ── Page Heading ───────────────────────── */
    .page-heading-wrap {{
        margin-bottom: 24px;
        animation: fadeInUp 0.4s ease;
    }}
    .page-heading {{
        font-weight: 650;
        font-size: 1.45rem;
        letter-spacing: -0.03em;
        color: {TEXT_PRIMARY};
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .page-heading-icon {{
        width: 32px;
        height: 32px;
        border-radius: 10px;
        background: {PRIMARY_GRADIENT};
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    .page-subtitle {{
        color: {TEXT_SECONDARY};
        font-size: 0.85rem;
        line-height: 1.4;
        margin-left: 42px;
    }}

    /* ── Badges ─────────────────────────────── */
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        white-space: nowrap;
    }}
    .badge-success {{
        background: rgba(16,185,129,0.12);
        color: {SUCCESS};
    }}
    .badge-warning {{
        background: rgba(245,158,11,0.12);
        color: {WARNING};
    }}
    .badge-danger {{
        background: rgba(239,68,68,0.12);
        color: {DANGER};
    }}
    .badge-info {{
        background: rgba(59,130,246,0.12);
        color: {INFO};
    }}

    /* ── Metric Mini Row ────────────────────── */
    .metric-row {{
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }}
    .metric-mini {{
        background: rgba(255,255,255,0.02);
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 8px 14px;
        flex: 1;
        min-width: 80px;
    }}
    .metric-mini-label {{
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {TEXT_MUTED};
        font-weight: 600;
    }}
    .metric-mini-value {{
        font-size: 0.95rem;
        font-weight: 600;
        color: {TEXT_PRIMARY};
        margin-top: 2px;
    }}

    /* ── Divider ────────────────────────────── */
    .rp-divider {{
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, {BORDER}, transparent);
        margin: 16px 0;
    }}

    /* ── Status Dot ─────────────────────────── */
    .status-dot {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        animation: pulseGlow 2s ease-in-out infinite;
    }}

    /* ── Alerts ─────────────────────────────── */
    .stAlert {{
        border-radius: 10px !important;
        border: none !important;
        animation: fadeIn 0.3s ease !important;
    }}

    /* ── Scrollbar ─────────────────────────── */
    ::-webkit-scrollbar {{ width: 4px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.06); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(255,255,255,0.12); }}

    /* ── Footer ────────────────────────────── */
    .app-footer {{
        text-align: center;
        color: {TEXT_MUTED};
        font-size: 0.72rem;
        padding-top: 20px;
        border-top: 1px solid {BORDER};
        margin-top: 48px;
        animation: fadeIn 0.6s ease;
    }}
    .app-footer span {{ color: {PRIMARY}; }}

    /* ── Skeleton Loading ───────────────────── */
    .skeleton {{
        background: linear-gradient(90deg, {BG_SURFACE} 25%, {BG_ELEVATED} 50%, {BG_SURFACE} 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s ease-in-out infinite;
        border-radius: 8px;
    }}
    .skeleton-text {{ height: 14px; margin-bottom: 8px; width: 80%; }}
    .skeleton-title {{ height: 12px; margin-bottom: 16px; width: 50%; }}
    .skeleton-card {{ height: 120px; margin-bottom: 16px; }}

    /* ── Sidebar Brand ──────────────────────── */
    .sidebar-brand {{
        padding: 18px 14px 4px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .sidebar-brand-icon {{
        width: 30px;
        height: 30px;
        background: {PRIMARY_GRADIENT};
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
        color: white;
        box-shadow: 0 2px 10px rgba(16,185,129,0.25);
        flex-shrink: 0;
    }}
    .sidebar-brand-text {{
        line-height: 1.2;
    }}
    .sidebar-brand-name {{
        color: {TEXT_PRIMARY};
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: -0.01em;
    }}
    .sidebar-brand-tag {{
        color: {PRIMARY};
        font-size: 0.5rem;
        letter-spacing: 0.2em;
        font-weight: 500;
        text-transform: uppercase;
    }}
</style>
"""

CORPORATE_LIGHT_CSS = f"""
<style>
    .stApp {{
        background:
            radial-gradient(circle at top right, rgba(37,99,235,0.08), transparent 34%),
            linear-gradient(180deg, #F7FAFF 0%, #FFFFFF 52%, #F8FBFF 100%) !important;
        color: {TEXT_PRIMARY} !important;
    }}

    [data-testid="stSidebar"] {{
        background: #FFFFFF !important;
        border-right: 1px solid {BORDER} !important;
        box-shadow: 12px 0 32px rgba(30,64,175,0.06);
    }}

    [data-testid="stSidebar"] * {{
        color: {TEXT_SECONDARY};
    }}

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {{
        color: {TEXT_SECONDARY} !important;
    }}

    .sidebar-brand-icon,
    .page-heading-icon,
    .kpi-card::before {{
        background: {PRIMARY_GRADIENT} !important;
    }}

    .sidebar-brand-icon {{
        box-shadow: 0 8px 22px rgba(37,99,235,0.22) !important;
    }}

    .sidebar-brand-name,
    .page-heading,
    .kpi-value,
    .section-header,
    .metric-mini-value {{
        color: {TEXT_PRIMARY} !important;
    }}

    .sidebar-brand-tag,
    .app-footer span {{
        color: {PRIMARY} !important;
    }}

    .stRadio div[role="radiogroup"] label {{
        border-radius: 8px;
        padding: 6px 8px;
        transition: background 0.2s ease, color 0.2s ease;
    }}

    .stRadio div[role="radiogroup"] label:hover {{
        background: #F1F5FF;
    }}

    .glass-panel,
    .kpi-card,
    .metric-mini {{
        background: #FFFFFF !important;
        border-color: {BORDER} !important;
        box-shadow: 0 16px 36px rgba(30,64,175,0.08) !important;
    }}

    .glass-panel:hover,
    .kpi-card:hover {{
        border-color: {BORDER_ACTIVE} !important;
        box-shadow: 0 18px 42px rgba(37,99,235,0.12) !important;
    }}

    .kpi-icon-wrap {{
        background: {PRIMARY_LIGHT} !important;
    }}

    .kpi-title,
    .page-subtitle,
    .metric-mini-label,
    .filter-label,
    .app-footer {{
        color: {TEXT_MUTED} !important;
    }}

    .stButton > button {{
        background: {PRIMARY_GRADIENT} !important;
        box-shadow: 0 8px 20px rgba(37,99,235,0.18) !important;
    }}

    .stButton > button:hover {{
        box-shadow: 0 12px 28px rgba(37,99,235,0.26) !important;
    }}

    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {{
        background: #FFFFFF !important;
        border-color: {BORDER} !important;
        color: {TEXT_PRIMARY} !important;
    }}

    .stDataFrame {{
        border-color: {BORDER} !important;
        box-shadow: 0 14px 32px rgba(30,64,175,0.06);
    }}

    .badge-success {{
        background: rgba(14,165,233,0.10) !important;
        color: #0369A1 !important;
    }}

    ::-webkit-scrollbar-thumb {{
        background: rgba(37,99,235,0.18);
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(37,99,235,0.30);
    }}
</style>
"""

SIDEBAR_BRAND = f"""
<div class="sidebar-brand">
    <div class="sidebar-brand-icon">RP</div>
    <div class="sidebar-brand-text">
        <div class="sidebar-brand-name">RetailPulse</div>
        <div class="sidebar-brand-tag">Intelligent Retail Engine</div>
    </div>
</div>
"""


def inject_global_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(CORPORATE_LIGHT_CSS, unsafe_allow_html=True)


def render_sidebar_brand():
    st.sidebar.markdown(SIDEBAR_BRAND, unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)


def render_kpi_card(title, value, icon_name="bar_chart", delta=None, delay=0):
    """Enhanced KPI card with gradient top-border and icon container."""
    delta_html = ""
    if delta is not None:
        c = SUCCESS if delta >= 0 else DANGER
        arrow = "↑" if delta >= 0 else "↓"
        delta_html = f'<div style="color:{c}; font-size:0.7rem; font-weight:500; margin-top:3px;">{arrow} {abs(delta):.1f}%</div>'
    st.markdown(f"""
        <div class="kpi-card" style="animation-delay:{delay}s;">
            <div class="kpi-icon-wrap">{icon(icon_name, size=20, color=PRIMARY)}</div>
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


def render_section_header(title, icon_name="trending_up"):
    """Section header with icon and bottom border."""
    st.markdown(
        f'<div class="section-header">{icon(icon_name, size=16, color=TEXT_PRIMARY)} {title}</div>',
        unsafe_allow_html=True
    )


def render_page_heading(title, subtitle=None, icon_name=None):
    """Page heading with optional gradient icon badge and subtitle."""
    icon_html = ""
    if icon_name:
        icon_html = f'<div class="page-heading-icon">{icon(icon_name, size=18, color="#fff")}</div>'
    heading = f'<div class="page-heading-wrap"><div class="page-heading">{icon_html}{title}</div>'
    if subtitle:
        heading += f'<div class="page-subtitle">{subtitle}</div>'
    heading += "</div>"
    st.markdown(heading, unsafe_allow_html=True)


def render_badge(label, variant="info"):
    """Small pill badge for statuses and tags."""
    variant_map = {
        "success": "badge-success",
        "warning": "badge-warning",
        "danger": "badge-danger",
        "info": "badge-info",
    }
    cls = variant_map.get(variant, "badge-info")
    st.markdown(f'<span class="badge {cls}">{label}</span>', unsafe_allow_html=True)


def render_divider():
    """Gradient horizontal divider."""
    st.markdown('<hr class="rp-divider">', unsafe_allow_html=True)


def render_metric_mini(label, value):
    """Compact inline metric display."""
    st.markdown(f"""
        <div class="metric-mini">
            <div class="metric-mini-label">{label}</div>
            <div class="metric-mini-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def chart_theme():
    """Plotly theme matching the corporate blue and white design system."""
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": TEXT_SECONDARY, "family": "Inter, sans-serif", "size": 10},
        "xaxis": {
            "gridcolor": "rgba(30,64,175,0.08)",
            "zerolinecolor": "rgba(30,64,175,0.12)",
            "tickfont": {"color": TEXT_MUTED, "size": 10},
        },
        "yaxis": {
            "gridcolor": "rgba(30,64,175,0.08)",
            "zerolinecolor": "rgba(30,64,175,0.12)",
            "tickfont": {"color": TEXT_MUTED, "size": 10},
        },
        "legend": {
            "font": {"color": TEXT_SECONDARY, "size": 10},
            "bgcolor": "rgba(0,0,0,0)",
        },
        "hoverlabel": {
            "bgcolor": BG_SURFACE,
            "font": {"color": TEXT_PRIMARY, "size": 10},
            "bordercolor": BORDER,
        },
    }


def glass_panel_start():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)


def glass_panel_end():
    st.markdown('</div>', unsafe_allow_html=True)


def render_footer():
    st.markdown(
        '<div class="app-footer">RetailPulse <span>AI</span> &bull; End-to-End Retail Intelligence Platform</div>',
        unsafe_allow_html=True
    )
