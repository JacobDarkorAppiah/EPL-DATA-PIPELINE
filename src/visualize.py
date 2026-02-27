import pandas as pd
import matplotlib.pyplot as plt
import os

def create_chart():
    # Path to your cleaned data
    path = os.path.join("data", "processed", "cleaned_epl_2025_2026.csv")
    
    if not os.path.exists(path):
        print("❌ Cleaned file not found! Run cleaning.py first.")
        return

    # Load data
    df = pd.read_csv(path)
    
    # Sort by points and take Top 10
    top_10 = df.sort_values(by='points', ascending=False).head(10)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.barh(top_10['team'], top_10['points'], color='skyblue')
    plt.xlabel('Points')
    plt.title('Premier League 2025-2026: Top 10 Standings')
    plt.gca().invert_yaxis()  # Highest points at the top
    
    print("🎨 Chart created! Closing the window will finish the script.")
    plt.show()

if __name__ == "__main__":
    create_chart()