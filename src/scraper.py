import os
import pandas as pd

def process_local_html():
    # Use the exact absolute path from your terminal output
    raw_dir = r"C:\EPL-PROJECT\EPL-DATA-PIPELINE\data\raw"
    html_path = os.path.join(raw_dir, "epl_stats.html")
    save_path = os.path.join(raw_dir, "epl_2025_2026.csv")

    print(f"🔄 Reading: {html_path}")

    if not os.path.exists(html_path):
        print("❌ ERROR: epl_stats.html is missing from the raw folder!")
        return

    try:
        # Read the HTML
        tables = pd.read_html(html_path)
        df = tables[0] # We know Table 0 is the one!

        # Clean the headers if they are messy
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(-1)

        # SAVE THE FILE
        df.to_csv(save_path, index=False)
        
        # VERIFY IT SAVED
        if os.path.exists(save_path):
            print(f"✅ SUCCESS! CSV created at: {save_path}")
            print(f"📏 File size: {os.path.getsize(save_path)} bytes")
        else:
            print("🚨 ERROR: Python said it saved, but the file is not there!")

    except Exception as e:
        print(f"🚨 Error: {e}")

if __name__ == "__main__":
    process_local_html()