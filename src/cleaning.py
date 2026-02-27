import pandas as pd
import os
import glob

def clean_epl_data():
    # 1. FIND ALL RAW FILES
    raw_path = "data/raw/*.csv"
    files = glob.glob(raw_path)
    
    if not files:
        print("⚠️ No raw files found. Run the scraper first!")
        return

    processed_data = []

    for file in files:
        print(f"🧹 Cleaning: {file}")
        df = pd.read_csv(file)

        # 2. DROP 'DUMMY' ROWS
        # FBref often includes extra header rows mid-table. We remove them.
        df = df[df['Squad'] != 'Squad']

        # 3. COLUMN RENAMING & SELECTION
        # We focus on the core stats: Matches Played, Wins, Draws, Losses, Goals For/Against, Points
        cols_to_keep = ['Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'Season']
        df = df[cols_to_keep]

        # 4. DATA TYPE CONVERSION
        # Ensure numbers are actually treated as numbers (integers)
        numeric_cols = ['MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

        # 5. MATHEMATICAL VALIDATION
        # In a 3-point system: (Wins * 3) + Draws should equal Points.
        # Also: Wins + Draws + Losses must equal Matches Played.
        integrity_check = df.apply(lambda row: (row['W'] + row['D'] + row['L']) == row['MP'], axis=1)
        
        if not integrity_check.all():
            print(f"🚨 Integrity Warning in {file}: Some rows have mismatched MP counts!")
        
        processed_data.append(df)

    # 6. MERGE ALL SEASONS INTO ONE MASTER FILE
    final_df = pd.concat(processed_data, ignore_index=True)
    
    # Ensure the processed directory exists
    os.makedirs("data/processed", exist_ok=True)
    
    output_file = "data/processed/epl_master_cleaned.csv"
    final_df.to_csv(output_file, index=False)
    print(f"✅ Cleaned data merged and saved to {output_file}")

if __name__ == "__main__":
    clean_epl_data()