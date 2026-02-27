import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright

def scrape_epl_data():
    # Use ABSOLUTE paths to avoid any confusion
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    save_path = os.path.join(raw_dir, "epl_2025_2026.csv")

    url = "https://fbref.com/en/comps/9/Premier-League-Stats"

    with sync_playwright() as p:
        user_data_dir = os.path.join(base_dir, "browser_session")
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            channel="msedge",
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = browser_context.pages[0]

        try:
            print(f"📡 Navigating to: {url}")
            page.goto(url)

            print("\n👋 INSTRUCTIONS:")
            print("1. Solve the Cloudflare box if it appears.")
            print("2. REFRESH the page if it stays stuck.")
            print("3. ONCE YOU SEE THE TABLE, come back here and press ENTER.")
            
            input(">>> Press ENTER here when the table is fully visible on your screen...")

            print("🔍 Extracting HTML...")
            content = page.content()
            
            # Debug: Check if 'Squad' even exists in the text
            if "Squad" in content:
                print("✅ Found 'Squad' in page source!")
            else:
                print("❌ 'Squad' NOT found in source. The scraper is seeing a blank page.")

            all_tables = pd.read_html(content)
            print(f"📊 Found {len(all_tables)} tables total.")

            league_table = None
            for i, df in enumerate(all_tables):
                if 'Squad' in str(df.columns) and 'Pts' in str(df.columns):
                    print(f"🎯 Target table found at index {i}!")
                    league_table = df
                    break

            if league_table is not None:
                if isinstance(league_table.columns, pd.MultiIndex):
                    league_table.columns = league_table.columns.get_level_values(-1)

                league_table = league_table.loc[:, ~league_table.columns.str.contains('^Unnamed')]
                
                # SAVE THE FILE
                league_table.to_csv(save_path, index=False)
                
                if os.path.exists(save_path):
                    print(f"🎉 SUCCESS! File verified at: {save_path}")
                else:
                    print("🚨 ERROR: Critical failure writing CSV to disk.")
            else:
                print("❌ ERROR: Could not find a table with 'Squad' and 'Pts'.")

        except Exception as e:
            print(f"🚨 ERROR: {e}")
        
        finally:
            browser_context.close()

if __name__ == "__main__":
    scrape_epl_data()