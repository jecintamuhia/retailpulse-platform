import os
import logging
import zipfile
import pandas as pd

logging.basicConfig(level=logging.INFO)


class RetailDataValidator:
    def __init__(self, raw_path: str, clean_path: str):
        self.raw_path = raw_path
        self.clean_path = clean_path

    def clean_raw_data(self) -> str:
        try:
            logging.info("Loading raw dataset...")
            logging.info(f"Reading file: {self.raw_path}")

            if not os.path.exists(self.raw_path):
                raise FileNotFoundError(
                    f"Dataset not found: {self.raw_path}"
                )

            # Verify XLSX file
            if not zipfile.is_zipfile(self.raw_path):
                raise ValueError(
                    f"Invalid Excel file: {self.raw_path}\n"
                    "The downloaded file is not a valid XLSX workbook.\n"
                    "Delete it and download again."
                )

            df = pd.read_excel(
                self.raw_path,
                engine="openpyxl"
            )

            logging.info(f"Initial rows: {len(df):,}")

            required_columns = [
                "InvoiceNo",
                "StockCode",
                "Quantity",
                "InvoiceDate",
                "UnitPrice",
                "CustomerID",
            ]

            missing = [
                col for col in required_columns
                if col not in df.columns
            ]

            if missing:
                raise ValueError(
                    f"Missing required columns: {missing}"
                )

            # Remove missing customers
            df = df.dropna(subset=["CustomerID"])
            df["CustomerID"] = (
                df["CustomerID"]
                .astype(int)
                .astype(str)
            )

            # Remove cancelled invoices
            df["InvoiceNo"] = (
                df["InvoiceNo"]
                .astype(str)
                .str.strip()
            )

            df = df[
                ~df["InvoiceNo"]
                .str.startswith("C", na=False)
            ]

            # Remove invalid transactions
            df = df[
                (df["Quantity"] > 0)
                & (df["UnitPrice"] > 0)
            ]

            # Format columns
            df["StockCode"] = (
                df["StockCode"]
                .astype(str)
                .str.strip()
            )

            df["InvoiceDate"] = pd.to_datetime(
                df["InvoiceDate"]
            )

            df["TotalRevenue"] = (
                df["Quantity"] * df["UnitPrice"]
            )

            # Remove duplicates
            df = df.drop_duplicates()

            os.makedirs(
                os.path.dirname(self.clean_path),
                exist_ok=True
            )

            df.to_csv(
                self.clean_path,
                index=False
            )

            logging.info(
                f"Cleaned rows: {len(df):,}"
            )

            logging.info(
                f"Saved cleaned data: {self.clean_path}"
            )

            return self.clean_path

        except Exception as e:
            logging.error(f"Cleaning failed: {e}")
            raise

    def validate_schema(self) -> bool:
        try:
            df = pd.read_csv(self.clean_path)

            checks = [
                df["CustomerID"].notnull().all(),
                (df["Quantity"] > 0).all(),
                (df["UnitPrice"] > 0).all(),
            ]

            if all(checks):
                logging.info("Validation PASSED")
                return True

            logging.error("Validation FAILED")
            return False

        except Exception as e:
            logging.error(
                f"Validation error: {e}"
            )
            return False