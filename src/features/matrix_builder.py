import pandas as pd
import numpy as np
def build_production_feature_store(cleaned_csv_path: str) -> tuple:
 df = pd.read_csv(cleaned_csv_path)
 df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
 max_date = df["InvoiceDate"].max()
 rfm = df.groupby("CustomerID").agg({
 "InvoiceDate": lambda x: (max_date - x.max()).days,
 "InvoiceNo": "nunique",
 "TotalRevenue": "sum"
 }).rename(columns={"InvoiceDate": "Recency", "InvoiceNo": "Frequency", "TotalRevenue":
"Monetary"})
 last_30 = df[df["InvoiceDate"] >= (max_date - pd.Timedelta(days=30))]
 active_ids = last_30["CustomerID"].unique()
 rfm["is_churned"] = np.where(rfm.index.isin(active_ids), 0, 1)
 df["Date"] = df["InvoiceDate"].dt.date
 ts = df.groupby("Date").agg({"Quantity": "sum", "TotalRevenue":
"sum"}).rename(columns={"Quantity": "items_sold", "TotalRevenue": "revenue"})
 ts["rolling_mean_7"] = ts["items_sold"].rolling(window=7).mean().fillna(method="bfill")
 return rfm.reset_index(), ts.reset_index()
