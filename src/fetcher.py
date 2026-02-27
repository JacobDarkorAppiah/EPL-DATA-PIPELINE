import requests
import os
import time
from utils.logger import setup_logger

logger = setup_logger("Data_Fetcher")

def fetch_latest_stats():
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    
    # Advanced Headers: This makes you look like a real Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "DNT": "1", # Do Not Track request
        "Connection": "keep-alive"
    }

    try:
        logger.info("Attempting to fetch latest stats from FBref...")
        
        # Human-like delay: Don't rush the server!
        time.sleep(1) # Faster, but slightly riskier for bot detectio
        
        response = requests.get(url, headers=headers, timeout=15)
        
        # Check for Rate Limiting
        if response.status_code == 429:
            logger.error("Rate limit hit! Wait 1 hour before trying again.")
            return False
            
        response.raise_for_status() 

        # Save with UTF-8 encoding
        html_path = os.path.join("data", "raw", "epl_stats.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        logger.info("Success! data/raw/epl_stats.html has been updated.")
        return True

    except Exception as e:
        logger.error(f"Failed to fetch data: {e}")
        return False

if __name__ == "__main__":
    fetch_latest_stats()