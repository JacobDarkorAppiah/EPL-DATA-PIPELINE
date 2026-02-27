import os
import pandas as pd
from bs4 import BeautifulSoup

def process_local_html():
    # Setup Paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(project_root, "data", "raw")
    html_path = os.path.join(raw_dir, "epl_stats.html")
    save_path = os.path.join(raw_dir, "epl_2025_2026.csv")

    print(f"🔍 Looking for local HTML file at: {html_path}")

    if not os.path.exists(html_path):
        print("❌ Error: 'epl_stats.html' not found in data/raw/!")
        print("💡 TIP: Open the site in Edge, press Ctrl+S, and save it as 'epl_stats.html' in that folder.")
        return

    try:
        print("📖 Reading local HTML file...")
        # We use 'lxml' or 'html.parser' to read the saved file
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tables = pd.read_html(content)
        print(f"📊 Found {len(tables)} tables in the file.")

        league_table = None
        for df in tables:
            # Flatten multi-index if it exists
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(-1)
            
            # Identify the correct table
            if 'Squad' in df.columns and 'Pts' in df.columns:
                league_table = df
                break

        if league_table is not None:
            # Clean up 'Unnamed' columns
            league_table = league_table.loc[:, ~league_table.columns.str.contains('^Unnamed')]
            
            # Save to CSV
            league_table.to_csv(save_path, index=False)
            print("-" * 50)
            print(f"🎉 SUCCESS! Local HTML converted to CSV: {save_path}")
            print(league_table[['RK', 'Squad', 'Pts']].head(5))
            print("-" * 50)
        else:
            print("❌ ERROR: Could not find the League Table in the saved HTML.")

    except Exception as e:
        print(f"🚨 CRITICAL ERROR: {e}")

if __name__ == "__main__":
    process_local_html()