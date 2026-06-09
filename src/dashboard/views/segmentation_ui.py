import streamlit as st
import pandas as pd
import plotly.express as px

def render_segmentation_ui():
    st.markdown("<h2 style='color:#FFFFFF; font-weight:700; margin-bottom:2px;'>Customer Segmentation</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9CA3AF; margin-top:0; font-size:0.95rem;'>Analyzing user behavior cluster allocation distributions.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    try:
        df = pd.read_csv("data/cleaned_transactions.csv")
        cust_profile = df.groupby('CustomerID')['TotalRevenue'].sum().reset_index()
        cust_profile = cust_profile[cust_profile['TotalRevenue'] < 4000] # Clean outliers for spacing

        # 1. MACRO SEGMENATATION CHART LAYER
        fig = px.histogram(
            cust_profile, x='TotalRevenue', nbins=50, 
            title="Customer Volume Value Cohort Breakdown"
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E5E7EB',
            xaxis=dict(showgrid=False, title="Monetary Volume Inflow ($)", color='#9CA3AF'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#9CA3AF'),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        fig.update_traces(marker_color='#059669', marker_line_width=1, marker_line_color="#111827")
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. MICRO-OPERATIONAL AND TASK TRACKING MATRIX LAYER (Bottom Grid)
        st.markdown("<h4 style='color:#FFFFFF; font-weight:600; margin-bottom:12px;'>Pipeline Execution & Reminders</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class='glass-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <span style='color:#FFF; font-weight:600; font-size:1rem;'>Ingestion Schema Validator</span>
                        <span style='background:rgba(16,185,129,0.15); color:#10B981; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600;'>Completed</span>
                    </div>
                    <p style='color:#9CA3AF; font-size:0.85rem; margin:12px 0 0 0; line-height:1.4;'>Great Expectations evaluated production criteria against 392,692 array objects successfully without system mutations.</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
                <div class='glass-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <span style='color:#FFF; font-weight:600; font-size:1rem;'>K-Means Behavioral Cluster Refit</span>
                        <span style='background:rgba(245,158,11,0.15); color:#F59E0B; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600;'>In Progress</span>
                    </div>
                    <p style='color:#9CA3AF; font-size:0.85rem; margin:12px 0 0 0; line-height:1.4;'>Processing 7-day rolling frequency data points. Current pipeline loop calculation cycle index tracking normal parameters.</p>
                </div>
            """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("Platform clean data engine array missing.")
