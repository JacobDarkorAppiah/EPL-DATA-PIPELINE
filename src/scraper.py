import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright

def scrape_epl_data():
    # Use absolute paths so there's NO guessing where the file goes
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(project_root, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    save_path = os.path.join(raw_dir, "epl_2025_2026.csv")

    url = "https://fbref.com/en/comps/9/Premier-League-Stats"

    with sync_playwright() as p:
        # We'll use a standard browser launch without the persistent profile for a 'fresh' try
        browser = p.chromium.launch(headless=False, channel="msedge")
        page = browser.new_page()

        try:
            print(f"📡 Navigating to: {url}")
            page.goto(url, wait_until="load", timeout=90000)

            print("\n🚨 ACTION REQUIRED:")
            print("1. If Cloudflare blocks you, click 'Verify'.")
            print("2. If the page is blank, REFRESH (F5).")
            print("3. Once the table with 'Arsenal', 'Man City' etc. is visible...")
            input(">>> Press ENTER here in the terminal to capture the data!")

            # Capture all tables on the page
            content = page.content()
            tables = pd.read_html(content)
            
            print(f"📊 Detected {len(tables)} tables. Looking for the League Standings...")

            found = False
            for df in tables:
                # FBref tables are often MultiIndex. Flatten them to check columns easily.
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(-1)
                
                # Check for the key indicators of the EPL table
                if 'Squad' in df.columns and 'Pts' in df.columns:
                    # Clean it up
                    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                    df['Season'] = '2025-2026'
                    
                    # SAVE IT
                    df.to_csv(save_path, index=False)
                    print(f"🎉 SUCCESS! File saved to: {save_path}")
                    print(df[['RK', 'Squad', 'Pts']].head(5))
                    found = True
                    break
            
            if not found:
                print("❌ ERROR: Could not find a table with 'Squad' and 'Pts'.")

        except Exception as e:
            print(f"🚨 CRITICAL ERROR: {e}")
        
        finally:
            browser.close()

if __name__ == "__main__":
    scrape_epl_data()