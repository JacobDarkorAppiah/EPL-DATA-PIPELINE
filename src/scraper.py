from playwright.sync_api import sync_playwright
import pandas as pd
import os
import time

def scrape_with_browser():
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    print("🚀 Launching invisible browser to bypass Cloudflare...")

    with sync_playwright() as p:
        # Change True to False so a window pops up on your screen
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # 1. Increase timeout to 60 seconds
            # 2. Only wait for the HTML structure (domcontentloaded), not the ads
            print("⏳ Navigating to FBref (this may take a minute)...")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # 3. Wait for the specific table to appear in the HTML
            print("🔍 Looking for the stats table...")
            page.wait_for_selector('table', timeout=15000)
            
            # Give it a tiny bit of time to settle
            time.sleep(3) 
            
            content = page.content()
            all_tables = pd.read_html(content)
            
            # ... (rest of your table finding logic stays the same)
            
            # Find the league table (the one with 'Squad' and 'Pts')
            league_table = None
            for df in all_tables:
                if 'Squad' in df.columns and 'Pts' in df.columns:
                    league_table = df
                    break
            
            if league_table is not None:
                # Clean up the table headers
                if isinstance(league_table.columns, pd.MultiIndex):
                    league_table.columns = league_table.columns.get_level_values(-1)
                
                league_table['Season'] = '2025-2026'
                
                # Save the file
                os.makedirs("data/raw", exist_ok=True)
                save_path = "data/raw/epl_2025_2026.csv"
                league_table.to_csv(save_path, index=False)
                
                print(f"✅ FINAL SUCCESS! File saved at: {save_path}")
                print(league_table.head(3))
            else:
                print("❌ Table not found on the page.")

        except Exception as e:
            print(f"🚨 Browser Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    scrape_with_browser()