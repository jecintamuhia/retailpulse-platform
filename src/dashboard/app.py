import streamlit as st

from views.forecasting_ui import render_forecasting_ui
from views.segmentation_ui import render_segmentation_ui
from views.executive_ui import render_executive_ui
from views.executive_ui_v2 import render_executive_ui_v2
from views.churn_ui import render_churn_ui
from ui_common import (
    inject_global_css, render_sidebar_brand, render_footer,
    render_page_heading, icon, TEXT_MUTED, TEXT_SECONDARY, PRIMARY
)

st.set_page_config(
    page_title="RetailPulse AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_global_css()

render_sidebar_brand()

pages = {
    "Executive Dashboard": "executive",
    "Command Center ": "executive_v2",
    "Forecasting": "forecasting",
    "Segmentation": "segmentation",
    "Churn Prediction": "churn",
}

page_labels = list(pages.keys())

selected = st.sidebar.radio(
    "Navigate",
    page_labels,
    index=page_labels.index(
        next((k for k, v in pages.items() if v == st.session_state.get("page", "executive")), "Executive Dashboard (v1)")
    ),
    key="nav_main",
)


page_map = {v: k for k, v in pages.items()}
st.session_state.page = pages[selected]

st.sidebar.markdown("---")

st.sidebar.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:8px; padding:6px 4px;">
        <span class="status-dot" style="background:{PRIMARY};"></span>
        <span style="color:{TEXT_SECONDARY}; font-size:0.85rem; font-weight:500;">Pipeline Ready</span>
    </div>
    """,
    unsafe_allow_html=True
)


st.sidebar.markdown(
    f"""
    <div style="margin-top:16px; padding:14px; border-radius:10px;
                background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.04);">
        <div style="color:{TEXT_MUTED}; font-size:0.65rem; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:4px; font-weight:600;">Platform</div>
        <div style="color:#F8FAFC; font-size:0.85rem; font-weight:500;">
            {icon("verified", size=14, color=PRIMARY)} v2.0 &mdash; Retail Intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

page = st.session_state.page

if page == "executive":
    render_executive_ui()
elif page == "executive_v2":
    render_executive_ui_v2()
elif page == "forecasting":
    render_forecasting_ui()
elif page == "segmentation":
    render_segmentation_ui()
elif page == "churn":
    render_churn_ui()

render_footer()
