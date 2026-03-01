import json
import pandas as pd
import os

def transform_data():
    raw_path = "data/raw/epl_standings.json"
    processed_path = "data/processed/epl_standings.csv"
    
    # 1. Load the JSON
    with open(raw_path, 'r') as f:
        data = json.load(f)
    
    # 2. Extract the table (this is the shortcut for Football-Data.org format)
    standings = data['standings'][0]['table']
    df = pd.json_normalize(standings)
    
    # 3. Clean up column names (e.g., 'team.name' -> 'team')
    df = df[['position', 'team.name', 'playedGames', 'won', 'draw', 'lost', 'points', 'goalsFor', 'goalsAgainst']]
    df.columns = ['rank', 'team', 'played', 'wins', 'draws', 'losses', 'pts', 'gf', 'ga']
    
    # 4. Save to CSV
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(processed_path, index=False)
    print(f"✅ Data transformed! Created {processed_path}")

if __name__ == "__main__":
    transform_data()