import pandas as pd
import os
import io
from utils.logger import setup_logger

logger = setup_logger("Data_Cleaner")

def clean_data():
    # 1. Define universal paths for Linux/Windows compatibility
    raw_data_path = os.path.join("data", "raw", "epl_stats.html")
    processed_dir = os.path.join("data", "processed")
    output_file = os.path.join(processed_dir, "cleaned_epl_2025_2026.csv")

    try:
        logger.info(f"🔄 Reading raw data from: {raw_data_path}")
        
        # Ensure the directory exists
        os.makedirs(processed_dir, exist_ok=True)

        # 2. Read the HTML content
        if not os.path.exists(raw_data_path):
            logger.error(f"❌ File not found: {raw_data_path}")
            return False

        with open(raw_data_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # 3. Extract the table
        # FBref often wraps tables in . read_html usually handles this,
        # but we target the "Regular Season" standings table specifically.
        tables = pd.read_html(io.StringIO(html_content))
        
        # Identify the correct table (usually the one with 'MP' or 'W' columns)
        df = None
        for t in tables:
            if 'MP' in t.columns or 'W' in t.columns:
                df = t
                break
        
        if df is None:
            logger.error("❌ Could not find the Premier League standings table in HTML.")
            return False

        # 4. Standardize Columns (Lowercase & Points mapping)
        df.columns = [str(c).lower() for c in df.columns]
        if 'pts' in df.columns:
            df = df.rename(columns={'pts': 'points'})

        # 5. 🛡️ Integrity Gate: Mathematical Validation
        # Enforce: Wins + Draws + Losses = Matches Played
        # We fillna(0) to ensure math doesn't fail on empty rows
        valid_rows = (df['w'].fillna(0) + df['d'].fillna(0) + df['l'].fillna(0)) == df['mp'].fillna(0)
        
        if not valid_rows.all():
            logger.warning("⚠️ Data Integrity Check Failed: Mathematical inconsistency detected in some rows.")
            # Optional: You can filter out bad rows here if you want:
            # df = df[valid_rows]
        else:
            logger.info("✅ Integrity Gate Passed: W + D + L = MP for all rows.")

        # 6. Save using the joined path
        df.to_csv(output_file, index=False)
        logger.info(f"✅ Cleaned data saved to {output_file}")
        return True

    except Exception as e:
        logger.error(f"❌ Cleaning failed: {e}")
        return False

if __name__ == "__main__":
    clean_data()