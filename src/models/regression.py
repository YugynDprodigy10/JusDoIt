# src/models/regression.py

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error

def train_regression_model(df, target='PTS'):
    df = df.copy()
    df['IS_POST_TRADE'] = (df['TRADE_PHASE'] == 'Post').astype(int)

    # Group by player & phase to get avg stats
    grouped = df.groupby(['PLAYER_NAME', 'TRADE_PHASE'])[target].mean().unstack()
    grouped['DELTA'] = grouped['Post'] - grouped['Pre']

    # Encode player as feature (optional for multiple players)
    grouped = grouped.dropna()
    X = pd.DataFrame({'IS_TRADED': 1}, index=grouped.index)
    y = grouped['DELTA']

    model = LinearRegression()
    model.fit(X, y)
    preds = model.predict(X)
    rmse = mean_squared_error(y, preds, squared=False)

    print(f"Model Coeff: {model.coef_[0]:.3f}, Intercept: {model.intercept_:.3f}, RMSE: {rmse:.3f}")
    return model

if __name__ == "__main__":
    df = pd.read_csv('data/processed/labeled_game_logs.csv')
    model = train_regression_model(df, target='PTS')