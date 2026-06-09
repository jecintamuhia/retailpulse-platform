import pandas as pd
from prophet import Prophet
def train_prophet_baseline(ts_df: pd.DataFrame):
 # Maps time matrices to explicit ds/y columns required by Prophet
 prophet_df = ts_df[["Date", "items_sold"]].rename(columns={"Date": "ds", "items_sold": "y"})
 model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
 model.fit(prophet_df)
 return model