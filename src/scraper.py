import cloudscraper
import pandas as pd
import os
from bs4 import BeautifulSoup

def scrape_universal():
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    scraper = cloudscraper.create_scraper()
    
    print("🚀 Running Universal Scraper (ID-Agnostic)...")
    
    try:
        response = scraper.get(url, timeout=15)
        
        # 1. Use Pandas to find ALL tables on the page
        all_tables = pd.read_html(response.text)
        
        # 2. Find the table that actually looks like a League Table
        # (It should have 'Squad' and 'Pts' columns)
        league_table = None
        for df in all_tables:
            if 'Squad' in df.columns and 'Pts' in df.columns:
                league_table = df
                break
        
        if league_table is not None:
            # Clean up Multi-Index columns if they exist
            if isinstance(league_table.columns, pd.MultiIndex):
                league_table.columns = league_table.columns.get_level_values(-1)
            
            league_table['Season'] = '2025-2026'
            
            # 3. FORCE SAVE
            os.makedirs("data/raw", exist_ok=True)
            save_path = os.path.join("data", "raw", "epl_2025_2026.csv")
            
            league_table.to_csv(save_path, index=False)
            
            # Final check to confirm file was actually written to disk
            if os.path.exists(save_path):
                print(f"✅ SUCCESS! File created at: {os.path.abspath(save_path)}")
                print(f"📊 Preview:\n{league_table.head(3)}")
            else:
                print("🚨 Error: Python said it saved, but the file is missing from disk.")
            
            return league_table
        else:
            print("❌ Could not find a table containing 'Squad' and 'Pts'.")

    except Exception as e:
        print(f"🚨 Critical Error: {e}")

if __name__ == "__main__":
    scrape_universal()