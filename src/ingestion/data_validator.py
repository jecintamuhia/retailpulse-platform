import os
import pandas as pd
import great_expectations as gx
from src.ingestion.stream_handler import RetailStreamHandler

class RetailDataValidator:
    def __init__(self, raw_path: str, clean_path: str):
        self.raw_path = raw_path
        self.clean_path = clean_path

    def clean_raw_data(self) -> str:
        """
        Cleans the real-world Online Retail dataset.
        Handles null CustomerIDs, cancels, and strips whitespace from StockCodes.
        """
        print("[*] Loading large-scale raw data into memory (this may take a moment)...")
        # Read the Excel file fetched from UCI
        df = pd.read_excel(self.raw_path)
        initial_count = len(df)
        print(f"[+] Loaded {initial_count:,} raw transactions.")

        # 1 & 2. Handle missing customer records and serialize type
        df = df.dropna(subset=["CustomerID"])
        df["CustomerID"] = df["CustomerID"].astype(int).astype(str)
        
        # 3. Handle retail cancellations (Invoice numbers starting with 'C')
        df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()
        df = df[~df["InvoiceNo"].str.startswith("C", na=False)]

        # 4. Enforce positive business metrics
        df = df[df["Quantity"] > 0]
        df = df[df["UnitPrice"] > 0.0]

        # 5. Data formatting and column additions
        df["StockCode"] = df["StockCode"].astype(str).str.strip()
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
        df["TotalRevenue"] = df["Quantity"] * df["UnitPrice"]

        # 6. Deduplicate entries
        df = df.drop_duplicates()

        # Save out to project directory
        os.makedirs(os.path.dirname(self.clean_path), exist_ok=True)
        df.to_csv(self.clean_path, index=False)
        
        print(f"[+] Cleaning complete. Rows processed from {initial_count:,} down to {len(df):,}.")
        print(f"[+] Validated clean file saved at: {self.clean_path}")
        return self.clean_path

    def validate_production_schema(self) -> bool:
        """Validates the processed real data against Great Expectations rules."""
        print("[*] Evaluating clean dataset with Great Expectations rules...")
        df = pd.read_csv(self.clean_path)
        
        # Convert standard Pandas DataFrame to Great Expectations dataset
        gx_df = gx.from_pandas(df)

        # 1. Validate Customer ID exists
        val_customer = gx_df.expect_column_values_to_not_be_null("CustomerID")["success"]
        
        # 2. Validate Quantity (>= 1) using range bound
        val_quantity = gx_df.expect_column_values_to_be_between(
            "Quantity", min_value=1, max_value=None
        )["success"]
        
        # 3. Validate UnitPrice (>= 0.01) using range bound
        val_price = gx_df.expect_column_values_to_be_between(
            "UnitPrice", min_value=0.01, max_value=None
        )["success"]

        # Aggregate logical checks
        all_passed = all([val_customer, val_quantity, val_price])
        
        if all_passed:
            print("[+] Schema Validation PASSED. Dataset is clean and ready for ML layers.")
        else:
            print("[-] Schema Validation FAILED. Unexpected records detected.")
            
        return all_passed

if __name__ == "__main__":
    # Complete automated sequence run
    raw_data_path = "data/raw_online_retail.xlsx"
    clean_data_path = "data/cleaned_transactions.csv"

    # Step 1: Stream real source data
    streamer = RetailStreamHandler()
    streamer.fetch_live_industry_data()

    # Step 2: Clean and validate real source data
    validator = RetailDataValidator(raw_path=raw_data_path, clean_path=clean_data_path)
    validator.clean_raw_data()
    validator.validate_production_schema()
