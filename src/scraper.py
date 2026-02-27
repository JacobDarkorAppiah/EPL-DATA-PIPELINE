import cloudscraper
import pandas as pd
import os

def scrape_simple():
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    scraper = cloudscraper.create_scraper()
    
    print("🚀 Attempting direct table extraction...")
    
    try:
        response = scraper.get(url)
        # Use Pandas to read the HTML directly from the response text
        # The 'match' parameter looks for a table containing the word 'Squad'
        all_tables = pd.read_html(response.text, attrs={'id': 'results2025-202691_overall'})
        
        if all_tables:
            df = all_tables[0]
            df['Season'] = '2025-2026'
            
            os.makedirs("data/raw", exist_ok=True)
            save_path = "data/raw/epl_2025_2026.csv"
            df.to_csv(save_path, index=False)
            
            print(f"✅ SUCCESS! File created at: {save_path}")
            return df
        else:
            print("❌ Table not found. FBref might have changed the Table ID.")

    except Exception as e:
        print(f"🚨 Error: {e}")

if __name__ == "__main__":
    scrape_simple()