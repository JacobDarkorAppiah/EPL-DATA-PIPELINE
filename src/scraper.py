import cloudscraper
from bs4 import BeautifulSoup, Comment
import pandas as pd
import os

def scrape_epl_season():
    # Target the 2025-2026 season
    season_name = "2025-2026"
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    
    print(f"🕵️‍♂️ Accessing data for {season_name} using Cloudscraper...")
    
    # Create a scraper instance that looks like a real browser
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    
    try:
        response = scraper.get(url, timeout=15)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # FBref often hides the main table in comments
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        
        for comment in comments:
            if 'id="results' in comment:
                table_soup = BeautifulSoup(comment, 'html.parser')
                df = pd.read_html(str(table_soup))[0]
                df['Season'] = season_name
                
                # Save the data
                os.makedirs("data/raw", exist_ok=True)
                save_path = f"data/raw/epl_{season_name.replace('-', '_')}.csv"
                df.to_csv(save_path, index=False)
                
                print(f"✅ SUCCESS! Saved {season_name} data to {save_path}")
                return df
                
        print("❌ HTML loaded, but couldn't find the stats table in comments.")
        
    except Exception as e:
        print(f"🚨 Still blocked! Error: {e}")

if __name__ == "__main__":
    scrape_epl_season()