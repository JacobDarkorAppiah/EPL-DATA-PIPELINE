import pandas as pd
import os

def clean_epl_data():
    # This gets the folder where cleaner.py is (src) and moves up to the main folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "epl_2025_2026.csv")
    processed_dir = os.path.join(base_dir, "data", "processed")
    save_path = os.path.join(processed_dir, "cleaned_epl_2025_2026.csv")

    print(f"🔍 Checking for file at: {raw_path}")

    if not os.path.exists(raw_path):
        print(f"❌ Error: File not found at the path above.")
        print("💡 TIP: Run 'python src/scraper.py' again and watch for the Success message.")
        return

    print("🧹 Starting Data Cleaning...")
    
    # Load data
    df = pd.read_csv(raw_path)
    
    # 1. Remove rows where 'Squad' is 'Squad' (FBref repeat headers)
    if 'Squad' in df.columns:
        df = df[df['Squad'] != 'Squad']
    
    # 2. Select columns we actually need for our model
    # We use a 'try-except' here in case the scraper grabbed different names
    try:
        cols_to_keep = {
            'RK': 'rank',
            'Squad': 'team',
            'MP': 'matches_played',
            'W': 'wins',
            'D': 'draws',
            'L': 'losses',
            'GF': 'goals_for',
            'GA': 'goals_against',
            'Pts': 'points'
        }
        df = df[list(cols_to_keep.keys())].rename(columns=cols_to_keep)
    except KeyError as e:
        print(f"⚠️ Warning: Missing some columns. Found: {df.columns.tolist()}")

    # 3. Save the cleaned data
    os.makedirs(processed_dir, exist_ok=True)
    df.to_csv(save_path, index=False)
    
    print("-" * 30)
    print(f"✅ CLEANING SUCCESS! Data saved to {save_path}")
    print(df.head())
    print("-" * 30)

if __name__ == "__main__":
    clean_epl_data()