import cloudscraper
import os
import time
from utils.logger import setup_logger

logger = setup_logger("Data_Fetcher")

def fetch_epl_data():
    # 1. Initialize the stealthy scraper here
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    
    try:
        logger.info("Attempting to fetch latest stats from FBref...")
        
        # Add a small delay to look more human
        time.sleep(3) 
        
        # 2. Use the 'scraper' object to get the page
        response = scraper.get(url)
        response.raise_for_status()

        # 3. Use Universal Paths (Works on Windows & Linux/GitHub)
        os.makedirs(os.path.join("data", "raw"), exist_ok=True)
        save_path = os.path.join("data", "raw", "epl_stats.html")

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        logger.info(f"✅ Successfully saved raw data to {save_path}")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to fetch data: {e}")
        return False

if __name__ == "__main__":
    fetch_epl_data()