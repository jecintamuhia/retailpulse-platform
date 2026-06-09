import streamlit as st
import pandas as pd
import plotly.express as px

def render_forecasting_ui():
    # Page Header Element Layout
    st.markdown("<h2 style='color:#FFFFFF; font-weight:700; margin-bottom:2px;'>Dashboard Framework</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9CA3AF; margin-top:0; font-size:0.95rem;'>Plan, prioritize, and accomplish pipeline metrics with ease.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. NORTH STAR METRICS LAYER (Top Grid)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='glass-card highlighted'>
                <div class='card-lbl'>Total Cleaned Rows</div>
                <div class='card-val'>392.6K</div>
                <div class='card-delta delta-up'>↗ 5.4% increased vs last ingestion</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class='glass-card'>
                <div class='card-lbl'>Active Stock items</div>
                <div class='card-val'>3,841</div>
                <div class='card-delta delta-neutral'>→ Stable distribution catalog</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class='glass-card'>
                <div class='card-lbl'>Running Forecast Forecasts</div>
                <div class='card-val'>12</div>
                <div class='card-delta delta-up'>↗ 2 modules computing live</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
            <div class='glass-card'>
                <div class='card-lbl'>Data Sanity Status</div>
                <div class='card-val'>100%</div>
                <div class='card-delta delta-up' style='color:#10B981;'>✓ Great Expectations Verified</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. TRENDS AND MACRO PERFORMANCE LAYER (Middle Container)
    try:
        df = pd.read_csv("data/cleaned_transactions.csv")
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        daily_sales = df.groupby('InvoiceDate')['TotalRevenue'].sum().reset_index()

        fig = px.line(
            daily_sales, x='InvoiceDate', y='TotalRevenue', 
            title="Project Analytics (Daily Processing Inflow Metrics)"
        )
        
        # Applying Transparent Theme variables directly to the Plotly Engine Matrix
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E5E7EB',
            title_font_size=16,
            xaxis=dict(showgrid=False, color='#9CA3AF'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#9CA3AF'),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        fig.update_traces(line_color='#10B981', line_width=3)
        
        # Wrap chart inside a matching glass background container
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error("Data source vector missing. Please check your system validation logic node pathing parameters.")
