# src/data_pipeline/clean_player_stats.py

import pandas as pd
import os

def label_trade_events(df):
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
    df = df.sort_values(by=["PLAYER_NAME", "GAME_DATE"]).reset_index(drop=True)
    
    df["TRADED"] = False
    df["TRADE_PHASE"] = "Pre"

    for player in df["PLAYER_NAME"].unique():
        player_df = df[df["PLAYER_NAME"] == player]
        teams = player_df["MATCHUP"].str.extract(r"([A-Z]{2,4})")

        if teams.nunique()[0] > 1:
            first_team = teams.iloc[0][0]
            trade_idx = teams[teams[0] != first_team].index[0]

            df.loc[(df["PLAYER_NAME"] == player) & (df.index >= trade_idx), "TRADED"] = True
            df.loc[(df["PLAYER_NAME"] == player) & (df.index >= trade_idx), "TRADE_PHASE"] = "Post"

    return df

if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)
    df = pd.read_csv("data/raw/game_logs.csv")
    df = label_trade_events(df)
    df["TEAM_ABBREVIATION"] = df["MATCHUP"].str.extract(r"^([A-Z]{2,4})")
    df.to_csv("data/processed/labeled_game_logs.csv", index=False)
    print("✅ Labeled game logs saved to data/processed/labeled_game_logs.csv")
