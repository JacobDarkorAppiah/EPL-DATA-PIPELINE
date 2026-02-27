import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time
import os

# 1. THE DISGUISE (To avoid the 403 Bouncer)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def scrape_epl_season(url, season_name):
    print(f"🕵️‍♂️ Accessing data for {season_name}...")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status() # Crash if we get a 403 or 404
        
        # 2. THE HUNT (Parsing Hidden Comments)
        # FBref hides many tables inside HTML comments soup = BeautifulSoup(response.text, 'html.parser')
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        
        # Look for the 'Regular Season' stats table within those comments
        for comment in comments:
            if 'id="results' in comment:
                table_soup = BeautifulSoup(comment, 'html.parser')
                df = pd.read_html(str(table_soup))[0]
                
                # Add a metadata column so we know which season this is
                df['Season'] = season_name
                
                # 3. THE STORAGE
                save_path = f"data/raw/epl_{season_name.replace('/', '_')}.csv"
                df.to_csv(save_path, index=False)
                print(f"✅ Successfully saved to {save_path}")
                return df
                
        print("❌ Could not find the table in the comments.")
        
    except Exception as e:
        print(f"🚨 Failed to scrape {season_name}: {e}")

if __name__ == "__main__":
    # Test with the current season
    target_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    scrape_epl_season(target_url, "2023-2024")