import pandas as pd
import numpy as np

def build_production_feature_store(cleaned_csv_path: str):
    df = pd.read_csv(cleaned_csv_path, parse_dates=["InvoiceDate"])

    df["CustomerID"] = df["CustomerID"].astype("category")
    max_date = df["InvoiceDate"].max()

   
    rfm = df.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda x: (max_date - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("TotalRevenue", "sum"),
    )

    stats = df.groupby("CustomerID").agg(
        avg_order_value=("TotalRevenue", "mean"),
        total_items=("Quantity", "sum"),
        unique_products=("StockCode", "nunique"),
    )

    rfm = rfm.join(stats)

    
    last_30 = df[df["InvoiceDate"] >= (max_date - pd.Timedelta(days=30))]
    active_ids = set(last_30["CustomerID"].unique())

    rfm["is_churned"] = (~rfm.index.isin(active_ids)).astype(int)

   
    df["Date"] = df["InvoiceDate"].dt.date

    ts = df.groupby("Date").agg(
        items_sold=("Quantity", "sum"),
        revenue=("TotalRevenue", "sum"),
    )

    ts["rolling_7"] = ts["items_sold"].rolling(7).mean().bfill()
    ts["rolling_30"] = ts["items_sold"].rolling(30).mean().bfill()
    ts["day_of_week"] = pd.to_datetime(ts.index).dayofweek
    ts["is_weekend"] = ts["day_of_week"].isin([5, 6]).astype(int)

    return rfm.reset_index(), ts.reset_index()