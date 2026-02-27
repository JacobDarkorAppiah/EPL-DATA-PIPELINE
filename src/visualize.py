import pandas as pd
import matplotlib.pyplot as plt
import os

def create_chart():
    # Path to your cleaned data
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(project_root, "data", "processed", "cleaned_epl_2025_2026.csv")
    
    if not os.path.exists(path):
        print(f"❌ Cleaned file not found at: {path}")
        return

    # Load data
    df = pd.read_csv(path)
    
    # --- THE FIX IS HERE ---
    # We use 'pts' because that's what the cleaner saved.
    # We use 'team' because the cleaner renamed 'squad' to 'team'.
    try:
        top_10 = df.sort_values(by='pts', ascending=False).head(10)

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.barh(top_10['team'], top_10['pts'], color='skyblue')
        plt.xlabel('Total Points')
        plt.ylabel('Football Club')
        plt.title('Premier League 2025-2026: Top 10 Standings')
        plt.gca().invert_yaxis()  # Put #1 at the top
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        print("🎨 Chart created! Look for the popup window.")
        plt.tight_layout()
        plt.show()
        
    except KeyError as e:
        print(f"❌ Column Name Error: {e}")
        print(f"Available columns in your file are: {df.columns.tolist()}")

if __name__ == "__main__":
    create_chart()