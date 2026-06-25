import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error


def train_prophet_baseline(ts_df: pd.DataFrame):
    df = ts_df.copy()

    # Ensure datetime
    df["Date"] = pd.to_datetime(df["Date"])

    
    if "is_weekend" not in df.columns:
        df["is_weekend"] = (
            df["Date"].dt.dayofweek >= 5
        ).astype(int)

    if "rolling_7" not in df.columns:
        df["rolling_7"] = (
            df["items_sold"]
            .rolling(window=7, min_periods=1)
            .mean()
        )

    prophet_df = df.rename(
        columns={
            "Date": "ds",
            "items_sold": "y"
        }
    )

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    model.add_regressor("is_weekend")
    model.add_regressor("rolling_7")

    model.fit(prophet_df)

    return model


def forecast_prophet(
    model,
    ts_df: pd.DataFrame,
    periods: int = 30
):
    df = ts_df.copy()

    df["Date"] = pd.to_datetime(df["Date"])

    future = model.make_future_dataframe(
        periods=periods
    )

    # Required regressor 1
    future["is_weekend"] = (
        future["ds"].dt.dayofweek >= 5
    ).astype(int)

    # Required regressor 2
    last_rolling_value = (
        df["items_sold"]
        .rolling(window=7, min_periods=1)
        .mean()
        .iloc[-1]
    )

    future["rolling_7"] = last_rolling_value

    forecast = model.predict(future)

    return forecast[
        [
            "ds",
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ]
    ]


def evaluate_prophet(
    model,
    ts_df: pd.DataFrame
):
    df = ts_df.copy()

    df["Date"] = pd.to_datetime(df["Date"])

    if "is_weekend" not in df.columns:
        df["is_weekend"] = (
            df["Date"].dt.dayofweek >= 5
        ).astype(int)

    if "rolling_7" not in df.columns:
        df["rolling_7"] = (
            df["items_sold"]
            .rolling(window=7, min_periods=1)
            .mean()
        )

    prophet_df = df.rename(
        columns={
            "Date": "ds",
            "items_sold": "y"
        }
    )

    forecast = model.predict(prophet_df)

    mae = mean_absolute_error(
        prophet_df["y"],
        forecast["yhat"]
    )

    print(
        f"Prophet MAE: {mae:.2f}"
    )

    return mae