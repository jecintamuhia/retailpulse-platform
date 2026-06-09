import streamlit as st
from src.dashboard.views.forecasting_ui import render_forecasting_ui
from src.dashboard.views.segmentation_ui import render_segmentation_ui

def main():
    st.set_page_config(page_title="RetailPulse Platform", layout="wide")

    # Injecting Advanced Global Glassmorphism UI Style Architecture
    st.markdown("""
        <style>
            /* Smooth background canvas gradient */
            .stApp {
                background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1f2937 100%) !important;
            }
            
            /* Sidebar Navigation Container Overhaul */
            [data-testid="stSidebar"] {
                background: rgba(255, 255, 255, 0.02) !important;
                backdrop-filter: blur(16px) !important;
                border-right: 1px solid rgba(255, 255, 255, 0.05);
            }
            
            /* Glassmorphism Metric / Progress Content Cards */
            .glass-card {
                background: rgba(255, 255, 255, 0.03) !important;
                backdrop-filter: blur(12px) !important;
                border: 1px solid rgba(255, 255, 255, 0.06) !important;
                border-radius: 16px !important;
                padding: 22px !important;
                margin-bottom: 16px;
                box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.25);
                transition: transform 0.2s ease, border-color 0.2s ease;
            }
            .glass-card:hover {
                border-color: rgba(16, 185, 129, 0.3);
                transform: translateY(-2px);
            }
            .glass-card.highlighted {
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(4, 120, 87, 0.03) 100%) !important;
                border: 1px solid rgba(16, 185, 129, 0.25) !important;
            }
            
            /* Card Typography Utilities */
            .card-lbl {
                color: #9CA3AF;
                font-size: 0.8rem !important;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                font-weight: 500;
            }
            .card-val {
                color: #FFFFFF;
                font-size: 2.1rem !important;
                font-weight: 700 !important;
                margin: 6px 0;
            }
            .card-delta {
                font-size: 0.8rem !important;
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 4px;
            }
            .delta-up { color: #10B981; }
            .delta-neutral { color: #9CA3AF; }
        </style>
    """, unsafe_allow_html=True)

    # Donezo Styling Sidebar Branding
    st.sidebar.markdown("<h1 style='color:#FFFFFF; font-weight:700; margin-bottom:0; font-size:2rem;'>RetailPulse</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color:#6B7280; font-size:0.85rem; margin-top:0; letter-spacing:0.05em;'>PLATFORM UTILITY ENGINE</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation Router Selection
    page = st.sidebar.radio("MENU NAVIGATION", ["📈 Demand Forecasting", "👥 Customer Segmentation"])

    st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("""
        <div style='background:rgba(255,255,255,0.02); padding:16px; border-radius:12px; border:1px solid rgba(255,255,255,0.05); text-align:center;'>
            <p style='color:#9CA3AF; font-size:0.8rem; margin-bottom:8px;'>Download our App</p>
            <button style='background:#10B981; color:white; border:none; padding:6px 16px; border-radius:6px; font-weight:600; font-size:0.8rem; cursor:pointer; width:100%;'>Get Local Node</button>
        </div>
    """, unsafe_allow_html=True)

    if "Demand Forecasting" in page:
        render_forecasting_ui()
    else:
        render_segmentation_ui()

if __name__ == "__main__":
    main()
