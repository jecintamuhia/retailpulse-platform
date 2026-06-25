import os
import sys
import logging
import joblib
import torch

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../"
        )
    )
)

from src.ingestion.stream_handler import RetailStreamHandler
from src.ingestion.data_validator import RetailDataValidator
from src.features.matrix_builder import build_production_feature_store
from src.models.customer_churn import execute_explainable_churn_training
from src.models.demand_lstm import train_lstm_model, forecast_lstm
from src.models.demand_prophet import (
    train_prophet_baseline,
    forecast_prophet,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

DATA_DIR = "data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
CLEAN_PATH = os.path.join(
    DATA_DIR,
    "cleaned",
    "transactions.csv"
)

FEATURE_DIR = os.path.join(
    DATA_DIR,
    "features"
)

MODEL_DIR = os.path.join(
    DATA_DIR,
    "models"
)


def run_pipeline():
    try:
        logging.info("Starting RetailPulse Pipeline")

        streamer = RetailStreamHandler(
            data_dir=RAW_DIR
        )

        raw_path = (
            streamer.fetch_live_industry_data()
        )

        logging.info(
            f"Dataset path: {raw_path}"
        )

        validator = RetailDataValidator(
            raw_path,
            CLEAN_PATH
        )

        clean_path = (
            validator.clean_raw_data()
        )

        if not validator.validate_schema():
            raise ValueError(
                "Data validation failed"
            )

        logging.info(
            "Building feature store..."
        )

        rfm, ts = (
            build_production_feature_store(
                clean_path
            )
        )

        os.makedirs(
            FEATURE_DIR,
            exist_ok=True
        )

        rfm.to_csv(
            os.path.join(
                FEATURE_DIR,
                "rfm.csv"
            ),
            index=False
        )

        ts.to_csv(
            os.path.join(
                FEATURE_DIR,
                "time_series.csv"
            ),
            index=False
        )

        logging.info(
            "Feature store saved"
        )

        logging.info(
            "Training churn model..."
        )

        churn_model, shap_values = (
            execute_explainable_churn_training(
                rfm
            )
        )

        os.makedirs(
            MODEL_DIR,
            exist_ok=True
        )

        joblib.dump(
            churn_model,
            os.path.join(
                MODEL_DIR,
                "churn_model.pkl"
            )
        )

        logging.info(
            "Churn model saved"
        )

        logging.info(
            "Training LSTM..."
        )

        lstm_model, scaler = (
            train_lstm_model(
                ts["items_sold"].values
            )
        )

        recent_data = (
            ts["items_sold"]
            .values[-30:]
        )

        lstm_forecast = (
            forecast_lstm(
                lstm_model,
                scaler,
                recent_data,
                steps=7
            )
        )

        torch.save(
            lstm_model.state_dict(),
            os.path.join(
                MODEL_DIR,
                "lstm_model.pt"
            )
        )

        logging.info(
            f"LSTM Forecast: {lstm_forecast}"
        )

        logging.info(
            "Training Prophet..."
        )

        prophet_model = (
            train_prophet_baseline(ts)
        )

        prophet_forecast = (
            forecast_prophet(
                prophet_model,
                ts,
                periods=7
            )
        )

        joblib.dump(
            prophet_model,
            os.path.join(
                MODEL_DIR,
                "prophet_model.pkl"
            )
        )

        forecast_dir = os.path.join(
            DATA_DIR,
            "forecasts"
        )

        os.makedirs(
            forecast_dir,
            exist_ok=True
        )

        prophet_forecast.to_csv(
            os.path.join(
                forecast_dir,
                "prophet_forecast.csv"
            ),
            index=False
        )

        logging.info(
            "Forecasts saved"
        )

        logging.info(
            "PIPELINE COMPLETED SUCCESSFULLY"
        )

        return {
            "churn_model": churn_model,
            "lstm_forecast": lstm_forecast,
            "prophet_forecast": prophet_forecast,
        }

    except Exception as e:
        logging.exception(
            f"Pipeline failed: {e}"
        )
        raise


if __name__ == "__main__":
    run_pipeline()