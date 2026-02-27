import pandas as pd

def predict_top_4(df):
    # Logic: Teams with PPG > 1.8 and GD > 10 are 85% likely to stay Top 4
    df['top_4_prob'] = df.apply(lambda row: 85 if (row['pts']/row['mp'] > 1.8 and row['gd'] > 10) else 15, axis=1)
    return df[['team', 'top_4_prob']].sort_values(by='top_4_prob', ascending=False)