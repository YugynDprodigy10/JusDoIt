import pandas as pd

def load_data(path="data/processed/with_bpm.csv"):
    df = pd.read_csv(path)
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
    df["SEASON"] = df["GAME_DATE"].dt.year.astype(str)
    return df

def filter_player_data(df, player_name, team=None, position=None, season=None):
    player_df = df[df["PLAYER_NAME"].str.lower() == player_name.lower()]
    if team:
        player_df = player_df[player_df["TEAM_ABBREVIATION"] == team]
    if position and "POSITION" in player_df.columns:
        player_df = player_df[player_df["POSITION"] == position]
    if season:
        player_df = player_df[player_df["SEASON"] == season]
    return player_df
