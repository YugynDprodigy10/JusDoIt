# src/data_pipeline/fetch_nba_stats.py

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import time

def get_player_id(player_name):
    all_players = players.get_players()
    player = [p for p in all_players if p['full_name'].lower() == player_name.lower()]
    return player[0]['id'] if player else None

def fetch_player_game_logs(player_name, season='2023'):
    player_id = get_player_id(player_name)
    if not player_id:
        print(f"Player {player_name} not found.")
        return None

    logs = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    df = logs.get_data_frames()[0]
    df['PLAYER_NAME'] = player_name
    return df

def batch_fetch_players(player_names, season='2023'):
    all_logs = []
    for name in player_names:
        print(f"Fetching: {name}")
        df = fetch_player_game_logs(name, season)
        if df is not None:
            all_logs.append(df)
        time.sleep(1)  # prevent rate limiting
    return pd.concat(all_logs, ignore_index=True)

if __name__ == "__main__":
    player_list = ['James Harden', 'Russell Westbrook', 'Kevin Durant']
    logs_df = batch_fetch_players(player_list, season='2023')
    logs_df.to_csv('data/raw/game_logs.csv', index=False)