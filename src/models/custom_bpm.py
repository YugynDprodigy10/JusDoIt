# src/models/custom_bpm.py

import pandas as pd

def calculate_ta_bpm(df):
    df = df.copy()
    df['IS_POST_TRADE'] = (df['TRADE_PHASE'] == 'Post').astype(int)

    # Basic version of BPM using weighted stats
    df['TA_BPM'] = (
        0.3 * df['PTS'] +
        0.2 * df['AST'] +
        0.15 * df['REB'] +
        0.1 * df['STL'] +
        0.1 * df['BLK'] -
        0.25 * df['TOV']
    )

    # Apply a trade penalty if in post-trade phase (you can tune this)
    df.loc[df['IS_POST_TRADE'] == 1, 'TA_BPM'] -= 0.5

    return df

if __name__ == "__main__":
    df = pd.read_csv('data/processed/labeled_game_logs.csv')
    df = calculate_ta_bpm(df)
    df.to_csv('data/processed/with_bpm.csv', index=False)