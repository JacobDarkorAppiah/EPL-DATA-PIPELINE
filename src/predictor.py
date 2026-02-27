import pandas as pd
import os

def load_data():
    path = os.path.join("data", "processed", "cleaned_epl_2025_2026.csv")
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)

def predict_match(home_team, away_team, df):
    # Find team stats
    home_stats = df[df['team'].str.lower() == home_team.lower()]
    away_stats = df[df['team'].str.lower() == away_team.lower()]

    if home_stats.empty or away_stats.empty:
        return "❌ One of those teams isn't in the database. Check your spelling!"

    # Calculate 'Power Score' (Points weighted + Goal Difference)
    # Higher score = Better form
    h_score = (home_stats['pts'].values[0] / home_stats['mp'].values[0]) + (home_stats['gd'].values[0] * 0.05)
    a_score = (away_stats['pts'].values[0] / away_stats['mp'].values[0]) + (away_stats['gd'].values[0] * 0.05)

    print(f"\n📊 Matchup: {home_team.title()} vs {away_team.title()}")
    print(f"🏠 {home_team.title()} Power Rating: {h_score:.2f}")
    print(f"🚀 {away_team.title()} Power Rating: {a_score:.2f}")

    if h_score > a_score + 0.2:
        return f"🔮 Result: CLEAR HOME WIN for {home_team.title()}"
    elif a_score > h_score + 0.2:
        return f"🔮 Result: CLEAR AWAY WIN for {away_team.title()}"
    else:
        return "🔮 Result: IT'S A TIGHT ONE! Likely a Draw or a 1-goal margin."

if __name__ == "__main__":
    data = load_data()
    if data is not None:
        print("⚽ WELCOME TO THE EPL PREDICTOR ⚽")
        team1 = input("Enter Home Team: ")
        team2 = input("Enter Away Team: ")
        print(predict_match(team1, team2, data))