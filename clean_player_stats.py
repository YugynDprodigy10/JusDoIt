# src/data_pipeline/clean_player_stats.py

import pandas as pd

def label_trade_events(df):
    df = df.sort_values(by=['PLAYER_NAME', 'GAME_DATE'])
    df['TRADED'] = False
    df['TRADE_PHASE'] = 'Pre'

    for player in df['PLAYER_NAME'].unique():
        player_df = df[df['PLAYER_NAME'] == player]
        teams = player_df['TEAM_ABBREVIATION'].unique()
        
        if len(teams) > 1:
            first_team = player_df.iloc[0]['TEAM_ABBREVIATION']
            trade_index = player_df[player_df['TEAM_ABBREVIATION'] != first_team].index[0]

            df.loc[(df['PLAYER_NAME'] == player) & (df.index >= trade_index), 'TRADED'] = True
            df.loc[(df['PLAYER_NAME'] == player) & (df.index >= trade_index), 'TRADE_PHASE'] = 'Post'

    return df

if __name__ == "__main__":
    df = pd.read_csv('data/raw/game_logs.csv')
    df = label_trade_events(df)
    df.to_csv('data/processed/labeled_game_logs.csv', index=False)