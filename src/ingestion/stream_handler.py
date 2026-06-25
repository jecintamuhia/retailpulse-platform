import requests
import os
import logging

logging.basicConfig(level=logging.INFO)

class RetailStreamHandler:
    def __init__(self, data_dir="data/raw"):
        self.data_dir = data_dir
        self.source_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
        self.output_path = os.path.join(self.data_dir, "online_retail.xlsx")

    def fetch_live_industry_data(self):
        if os.path.exists(self.output_path):
            logging.info(f"Dataset already exists: {self.output_path}")
            return self.output_path

        os.makedirs(self.data_dir, exist_ok=True)

        try:
            logging.info("Downloading dataset...")
            response = requests.get(self.source_url, stream=True, timeout=30)
            response.raise_for_status()

            with open(self.output_path, "wb") as f:
                for chunk in response.iter_content(8192):
                    if chunk:
                        f.write(chunk)

            logging.info("Download complete.")
            return self.output_path

        except requests.exceptions.RequestException as e:
            logging.error(f"Download failed: {e}")
            raise