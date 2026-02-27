def calculate_trend(df):
    # Goals per game trend
    df['goal_efficiency'] = df['gd'] / df['mp']
    return df[['team', 'goal_efficiency']].sort_values(by='goal_efficiency', ascending=False)