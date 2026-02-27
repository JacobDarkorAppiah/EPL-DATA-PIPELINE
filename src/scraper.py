import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright

def scrape_epl_data():
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    raw_dir = os.path.join("data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    save_path = os.path.join(raw_dir, "epl_2025_2026.csv")

    print("🚀 Launching Edge with Persistent Human Profile...")

    with sync_playwright() as p:
        # This creates a folder to save your 'human' session
        user_data_dir = "./browser_session"
        
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            channel="msedge",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={'width': 1280, 'height': 800}
        )
        
        page = browser_context.pages[0]

        try:
            print(f"📡 Navigating to FBref...")
            page.goto(url, wait_until="commit", timeout=90000)

            print("🛑 ACTION REQUIRED:")
            print("1. If there is a checkbox, click it.")
            print("2. If the page stays stuck, REFRESH the Edge window manually.")
            print("3. I will wait until I see the word 'Squad' on the screen...")
            
            # Wait up to 2 minutes for you to solve the puzzle
            page.wait_for_selector("text=Squad", timeout=120000)
            
            print("✅ 'Squad' detected! Reading tables...")
            time.sleep(5) # Let the table finish drawing

            content = page.content()
            all_tables = pd.read_html(content)
            
            league_table = None
            for df in all_tables:
                col_text = str(df.columns.tolist())
                if 'Squad' in col_text and 'Pts' in col_text:
                    league_table = df
                    break

            if league_table is not None:
                if isinstance(league_table.columns, pd.MultiIndex):
                    league_table.columns = league_table.columns.get_level_values(-1)

                league_table = league_table.loc[:, ~league_table.columns.str.contains('^Unnamed')]
                league_table['Season'] = '2025-2026'
                league_table.to_csv(save_path, index=False)

                print("-" * 50)
                print(f"🎉 SUCCESS! Data saved at: {save_path}")
                print(league_table[['RK', 'Squad', 'Pts']].head(5))
                print("-" * 50)
            else:
                print("❌ ERROR: Found the page but couldn't parse the table.")

        except Exception as e:
            print(f"🚨 ERROR: {e}")
        
        finally:
            print("👋 Closing browser...")
            browser_context.close()

if __name__ == "__main__":
    scrape_epl_data()