import pandas as pd
import os

def clean_epl_data():
    # 1. Define Paths (using absolute paths to prevent errors)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(project_root, "data", "raw", "epl_2025_2026.csv")
    processed_dir = os.path.join(project_root, "data", "processed")
    processed_path = os.path.join(processed_dir, "cleaned_epl_2025_2026.csv")

    print(f"🔍 Looking for raw file at: {raw_path}")

    # 2. Check if the file exists
    if not os.path.exists(raw_path):
        print("❌ Error: Still can't find the raw CSV.")
        print("💡 Check your data/raw/ folder in VS Code. Is there a file there?")
        return

    # 3. Load and Clean
    try:
        df = pd.read_csv(raw_path)
        print("📖 Raw data loaded successfully!")

        # Basic Cleaning
        # Rename columns to lowercase for easier coding
        df.columns = [col.lower() for col in df.columns]

        # Select only the columns we need for analysis
        # (Using 'rk' instead of 'rank' because that's how FBref exports it)
        cols_to_keep = ['rk', 'squad', 'mp', 'w', 'd', 'l', 'pts', 'gd']
        df_cleaned = df[cols_to_keep].copy()

        # Rename 'squad' to 'team' for a cleaner look
        df_cleaned = df_cleaned.rename(columns={'squad': 'team'})

        # 4. Save the cleaned file
        os.makedirs(processed_dir, exist_ok=True)
        df_cleaned.to_csv(processed_path, index=False)

        print("-" * 30)
        print(f"✅ SUCCESS: Cleaned data saved to {processed_path}")
        print(df_cleaned.head())
        print("-" * 30)

    except Exception as e:
        print(f"🚨 Cleaning Error: {e}")

if __name__ == "__main__":
    clean_epl_data()