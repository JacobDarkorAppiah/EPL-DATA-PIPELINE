import pandas as pd
import os
from utils.logger import setup_logger

logger = setup_logger("Data_Cleaner")

def clean_data():
    # 1. Define universal paths
    raw_data_path = os.path.join("data", "raw", "epl_stats.html")
    processed_dir = os.path.join("data", "processed")
    output_file = os.path.join(processed_dir, "cleaned_epl_2025_2026.csv")

    try:
        logger.info(f"🔄 Reading raw data from: {raw_data_path}")
        
        # Ensure the directory exists
        os.makedirs(processed_dir, exist_ok=True)

        # ... your existing scraping/cleaning logic here ...
        # df = pd.read_html(raw_data_path)...

        # 2. Save using the joined path
        df.to_csv(output_file, index=False)
        logger.info(f"✅ Cleaned data saved to {output_file}")
        return True

    except Exception as e:
        logger.error(f"❌ Cleaning failed: {e}")
        return False