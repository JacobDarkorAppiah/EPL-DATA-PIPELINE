import requests
import os
import json
from dotenv import load_dotenv
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger("Data_Fetcher")

def fetch_epl_data():
    api_key = os.getenv("FOOTBALL_DATA_API_KEY")
    # This URL gets the current Premier League Standings
    url = "https://api.football-data.org/v4/competitions/PL/standings"
    
    headers = { 'X-Auth-Token': api_key }

    try:
        logger.info("📡 Fetching EPL standings from API...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()

        # Save as JSON (much easier to handle than HTML!)
        os.makedirs(os.path.join("data", "raw"), exist_ok=True)
        save_path = os.path.join("data", "raw", "epl_standings.json")

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
        logger.info(f"✅ Success! Data saved to {save_path}")
        return True

    except Exception as e:
        logger.error(f"❌ API Error: {e}")
        return False

if __name__ == "__main__":
    fetch_epl_data()