import pandas as pd
import os

def extract_league_table():
    # Setup Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "data", "raw", "epl_stats.html")
    output_dir = os.path.join(base_dir, "data", "processed")
    output_path = os.path.join(output_dir, "cleaned_epl_2025_2026.csv")
    
    os.makedirs(output_dir, exist_ok=True)

    # Read the HTML file
    print(f"📖 Reading tables from {input_path}...")
    tables = pd.read_html(input_path)

    # Grab the target table (Table 0)
    df = tables[0]
    
    # Basic Cleanup: 
    # 1. Remove rows that might be empty or repeating headers
    df = df[df['Squad'] != 'Squad'] 
    
    # 2. Save to CSV
    df.to_csv(output_path, index=False)
    
    print(f"✅ Success! Extracted table saved to: {output_path}")
    print("\n--- PREVIEW ---")
    print(df[['Rk', 'Squad', 'Pts']].head())

if __name__ == "__main__":
    extract_league_table()