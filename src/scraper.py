import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import os

# 1. THE UPDATED DISGUISE
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

def scrape_epl_season(url, season_name):
    print(f"🕵️‍♂️ Accessing data for {season_name}...")
    session = requests.Session() 
    
    try:
        # The code that might fail
        response = session.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        
        for comment in comments:
            if 'id="results' in comment:
                table_soup = BeautifulSoup(comment, 'html.parser')
                df = pd.read_html(str(table_soup))[0]
                df['Season'] = season_name
                
                os.makedirs("data/raw", exist_ok=True)
                save_path = f"data/raw/epl_{season_name.replace('/', '_')}.csv"
                df.to_csv(save_path, index=False)
                print(f"✅ Successfully saved to {save_path}")
                return df
                
    except Exception as e:
        # The safety net that catches the error
        print(f"🚨 Failed to scrape {season_name}: {e}")

if __name__ == "__main__":
    target_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    scrape_epl_season(target_url, "2023-2024")
