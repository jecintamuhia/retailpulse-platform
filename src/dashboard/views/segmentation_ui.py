import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from ui_common import (
    render_section_header, chart_theme, render_kpi_card,
    glass_panel_start, glass_panel_end, render_page_heading,
    CHART_COLORS, TEXT_SECONDARY
)

DATA_PATH = "data/cleaned/transactions.csv"


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
def compute_segments(df):
    customer = (
        df.groupby('CustomerID')
        .agg({'InvoiceNo': 'nunique', 'TotalRevenue': 'sum'})
        .reset_index()
    )

    customer.columns = ['CustomerID', 'Frequency', 'Monetary']

    # Remove extreme outliers
    monetary_cap = customer['Monetary'].quantile(0.99)
    customer = customer[customer['Monetary'] < monetary_cap]

    scaler = StandardScaler()
    X = scaler.fit_transform(customer[['Frequency', 'Monetary']])

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    customer['Cluster'] = kmeans.fit_predict(X)

    cluster_map = {0: "Standard", 1: "High Value", 2: "VIP"}
    customer['Segment'] = customer['Cluster'].map(cluster_map)

    return customer


def render_segmentation_ui():
    render_page_heading(
        "Customer Segmentation",
        subtitle="Explore customer clusters, product affinities, and buying behaviour patterns.",
        icon_name="diversity_3"
    )

    try:
        df = load_data()
        segments = compute_segments(df)

        total_customers = segments['CustomerID'].nunique()
        vip_count = len(segments[segments['Segment'] == 'VIP'])
        high_value_count = len(segments[segments['Segment'] == 'High Value'])

        # ── KPIs ──
        cols = st.columns(4)
        with cols[0]:
            render_kpi_card("Total Customers", f"{total_customers:,}", icon_name="group")
        with cols[1]:
            render_kpi_card("VIP", f"{vip_count:,}", icon_name="star")
        with cols[2]:
            render_kpi_card("High Value", f"{high_value_count:,}", icon_name="diamond")
        with cols[3]:
            segment_pct = f"{(vip_count / total_customers * 100):.1f}%" if total_customers else "0%"
            render_kpi_card("VIP Share", segment_pct, icon_name="bar_chart")

        st.markdown("<br>", unsafe_allow_html=True)

        col_left, col_right = st.columns(2)

        # ── Scatter Plot ──
        with col_left:
            glass_panel_start()
            render_section_header("Customer Segment Clusters", icon_name="trackpad_target")

            segment_colors = {
                "Standard": CHART_COLORS[3],
                "High Value": CHART_COLORS[5],
                "VIP": CHART_COLORS[0]
            }

            fig = px.scatter(
                segments,
                x='Frequency',
                y='Monetary',
                color='Segment',
                color_discrete_map=segment_colors,
                template="plotly_dark",
                size='Monetary',
                size_max=18,
                hover_data={
                    'CustomerID': True,
                    'Frequency': ':.0f',
                    'Monetary': ':.0f'
                }
            )

            fig.update_layout(
                height=450,
                xaxis_title="Purchase Frequency",
                yaxis_title="Total Spend",
                **chart_theme()   # ✅ legend handled here only
            )

            fig.update_traces(
                marker=dict(line=dict(width=1, color='rgba(0,0,0,0.3)'))
            )

            st.plotly_chart(fig, width='stretch')
            glass_panel_end()

        # ── Pie Chart ──
        with col_right:
            glass_panel_start()
            render_section_header("Segment Distribution", icon_name="pie_chart")

            seg_counts = segments['Segment'].value_counts().reset_index()
            seg_counts.columns = ['Segment', 'Customers']

            fig = px.pie(
                seg_counts,
                names='Segment',
                values='Customers',
                color='Segment',
                color_discrete_map={
                    "Standard": CHART_COLORS[3],
                    "High Value": CHART_COLORS[5],
                    "VIP": CHART_COLORS[0]
                },
                hole=0.55
            )

            fig.update_traces(
                textinfo="label+percent",
                textfont=dict(size=11)
            )

            # ❌ REMOVED legend=... to avoid conflict
            fig.update_layout(
                height=450,
                showlegend=True,
                **chart_theme()
            )

            st.plotly_chart(fig, width='stretch')
            glass_panel_end()

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Product Affinity Matrix ──
        glass_panel_start()
        render_section_header("Product Affinity Matrix", icon_name="link")

        top_products = df['StockCode'].value_counts().nlargest(10).index
        basket = df[df['StockCode'].isin(top_products)]

        pivot = basket.groupby(['InvoiceNo', 'StockCode']).size().unstack(fill_value=0)
        pivot = pivot.applymap(lambda x: 1 if x > 0 else 0)

        corr = pivot.corr()

        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale=px.colors.sequential.Emrld_r,
            aspect="auto"
        )

        fig.update_layout(
            height=450,
            **chart_theme()
        )

        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(tickangle=-45)

        st.plotly_chart(fig, width='stretch')
        glass_panel_end()

    except Exception as e:
        st.error(f"Error loading segmentation view: {e}")