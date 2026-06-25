import streamlit as st
import pandas as pd
import plotly.express as px
import os
from ui_common import (
    render_section_header, chart_theme,
    glass_panel_start, glass_panel_end,
    render_kpi_card, render_page_heading,
    CHART_COLORS
)

DATA_PATH = "data/cleaned/transactions.csv"
FORECAST_PATH = "data/forecasts/prophet_forecast.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    if "TotalRevenue" not in df.columns and "TotalPrice" not in df.columns:
        df["TotalRevenue"] = df["Quantity"] * df["UnitPrice"]
    elif "TotalRevenue" not in df.columns:
        df["TotalRevenue"] = df["TotalPrice"]
    return df


@st.cache_data
def load_forecast():
    if os.path.exists(FORECAST_PATH):
        forecast = pd.read_csv(FORECAST_PATH)
        forecast['ds'] = pd.to_datetime(forecast['ds'])
        return forecast
    return None


def render_forecasting_ui():
    render_page_heading(
        "Demand Forecasting & Velocity",
        subtitle="Historical revenue trends, hourly order velocity, and ML-powered demand predictions.",
        icon_name="trending_up"
    )

    try:
        df = load_data()

        # ── KPIs (staggered entrance) ──
        total_revenue = df['TotalRevenue'].sum()
        total_days = df['InvoiceDate'].dt.date.nunique()
        avg_daily = total_revenue / total_days if total_days else 0

        cols = st.columns(3)
        with cols[0]:
            render_kpi_card("Total Revenue", f"${total_revenue:,.0f}", icon_name="payments", delay=0.0)
        with cols[1]:
            render_kpi_card("Days of Data", f"{total_days}", icon_name="calendar_month", delay=0.05)
        with cols[2]:
            render_kpi_card("Avg Daily Revenue", f"${avg_daily:,.0f}", icon_name="bar_chart", delay=0.10)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Historical Revenue ──
        glass_panel_start()
        render_section_header("Historical Revenue", icon_name="trending_up")
        daily = df.groupby(df['InvoiceDate'].dt.date)['TotalRevenue'].sum().reset_index()
        daily.columns = ['Date', 'Revenue']
        fig = px.line(
            daily, x='Date', y='Revenue',
            color_discrete_sequence=[CHART_COLORS[0]],
            template="plotly_dark"
        )
        fig.update_traces(line=dict(width=2.5), fill="tozeroy", fillcolor="rgba(16,185,129,0.05)")
        fig.update_layout(height=350, showlegend=False, **chart_theme())
        st.plotly_chart(fig, width='stretch')
        glass_panel_end()

        col_left, col_right = st.columns(2)

        with col_left:
            # ── Hourly Orders ──
            glass_panel_start()
            render_section_header("Hourly Order Velocity", icon_name="schedule")
            df['Hour'] = df['InvoiceDate'].dt.hour
            hourly = df.groupby('Hour')['InvoiceNo'].nunique().reset_index()
            hourly.columns = ['Hour', 'Orders']
            fig = px.bar(
                hourly, x='Hour', y='Orders',
                color_discrete_sequence=[CHART_COLORS[0]],
                template="plotly_dark"
            )
            fig.update_traces(
                marker=dict(line=dict(width=0)),
                hovertemplate="Hour %{x}:00<br>%{y} orders<extra></extra>"
            )
            fig.update_layout(height=300, showlegend=False, **chart_theme())
            fig.update_xaxes(tickmode="array", tickvals=list(range(0, 24, 2)))
            st.plotly_chart(fig, width='stretch')
            glass_panel_end()

        with col_right:
            # ── Forecast ──
            glass_panel_start()
            render_section_header("7-Day ML Forecast", icon_name="auto_graph")
            forecast = load_forecast()
            if forecast is not None:
                fig = px.line(
                    forecast, x='ds', y='yhat',
                    color_discrete_sequence=[CHART_COLORS[0]],
                    template="plotly_dark"
                )
                fig.update_traces(line=dict(width=2.5))
                if 'yhat_lower' in forecast.columns and 'yhat_upper' in forecast.columns:
                    fig.add_scatter(
                        x=forecast['ds'], y=forecast['yhat_upper'],
                        mode='lines', line=dict(width=0), showlegend=False
                    )
                    fig.add_scatter(
                        x=forecast['ds'], y=forecast['yhat_lower'],
                        mode='lines', line=dict(width=0),
                        fill='tonexty', fillcolor='rgba(16,185,129,0.12)',
                        showlegend=False
                    )
                fig.update_layout(
                    height=300, showlegend=False,
                    xaxis_title=None, yaxis_title="Predicted Revenue",
                    **chart_theme()
                )
                st.plotly_chart(fig, width='stretch')
            else:
                st.info(
                    "No forecast available. Run the training pipeline to generate a 7-day Prophet forecast.",
                    icon="ℹ️"
                )
            glass_panel_end()

    except Exception as e:
        st.error(f"Error loading forecasting view: {e}")