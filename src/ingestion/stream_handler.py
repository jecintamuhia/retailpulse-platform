import os
import requests

class RetailStreamHandler:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        # UCI Machine Learning Repository URL for real UK Retail transaction data
        self.source_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
        self.raw_output_path = os.path.join(self.data_dir, "raw_online_retail.xlsx")

    def fetch_live_industry_data(self) -> str:
        """Downloads the real-world 500k+ row retail dataset programmatically."""
        if os.path.exists(self.raw_output_path):
            print(f"[+] Raw industry data already exists locally at: {self.raw_output_path}")
            return self.raw_output_path

        print(f"[*] Fetching live industry dataset from UCI Repository...")
        print(f"[*] Target URL: {self.source_url}")
        os.makedirs(self.data_dir, exist_ok=True)
        
        response = requests.get(self.source_url, stream=True)
        if response.status_code == 200 or response.ok:
            with open(self.raw_output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f" Download complete. Saved to {self.raw_output_path}")
        else:
            raise ConnectionError(f" Failed to fetch data from source. Status code: {response.status_code}")
            
        return self.raw_output_path

if __name__ == "__main__":
    handler = RetailStreamHandler()
    handler.fetch_live_industry_data()
