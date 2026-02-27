import requests
import os
from utils.logger import setup_logger

logger = setup_logger("Data_Fetcher")

def fetch_latest_stats():
    # The URL for the 2025-2026 PL Season
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    
    # We must pretend to be a real browser (Chrome) to avoid a 403 Forbidden error
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        logger.info("🌐 Fetching latest stats from FBref...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Check if the request was successful

        # Save the new HTML over the old one
        html_path = os.path.join("data", "raw", "epl_stats.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        logger.info("✅ Success! data/raw/epl_stats.html has been updated.")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to fetch data: {e}")
        return False

if __name__ == "__main__":
    fetch_latest_stats()