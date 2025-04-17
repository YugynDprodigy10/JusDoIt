# src/viz/plot_trade_impact.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Style settings
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# -----------------------------------
# Load data
# -----------------------------------
def load_data(path="data/processed/with_bpm.csv"):
    df = pd.read_csv(path)
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
    return df

# -----------------------------------
# PPG Change Bar Plot
# -----------------------------------
def plot_ppg_change_bar(df, save=False):
    avg_stats = df.groupby(["PLAYER_NAME", "TRADE_PHASE"])[["PTS"]].mean().reset_index()
    pivot = avg_stats.pivot(index="PLAYER_NAME", columns="TRADE_PHASE")
    pivot.columns = ["PPG_Pre", "PPG_Post"]
    pivot["PPG_Diff"] = pivot["PPG_Post"] - pivot["PPG_Pre"]
    pivot = pivot.dropna().sort_values(by="PPG_Diff")

    fig, ax = plt.subplots()
    pivot["PPG_Diff"].plot(kind="barh", ax=ax, color="coral")
    ax.set_title("Change in PPG After Trade")
    ax.set_xlabel("Δ PPG")
    plt.tight_layout()

    if save:
        os.makedirs("screenshots", exist_ok=True)
        fig.savefig("screenshots/ppg_change_bar.png")
    
    plt.show()

# -----------------------------------
# Boxplot of TA-BPM Pre/Post
# -----------------------------------
def plot_bpm_boxplot(df, save=False):
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="TRADE_PHASE", y="TA_BPM", ax=ax)
    ax.set_title("TA-BPM Distribution: Pre vs Post Trade")
    plt.tight_layout()

    if save:
        os.makedirs("screenshots", exist_ok=True)
        fig.savefig("screenshots/bpm_boxplot.png")

    plt.show()

# -----------------------------------
# Multi-Stat Timeline for a Player
# -----------------------------------
def plot_player_timeline(df, player_name, stats=["PTS", "AST", "REB", "TA_BPM"], save=False):
    player_df = df[df["PLAYER_NAME"] == player_name].sort_values("GAME_DATE")

    fig, ax = plt.subplots(figsize=(12, 6))

    for stat in stats:
        ax.plot(player_df["GAME_DATE"], player_df[stat], marker="o", label=stat)

    if "Post" in player_df["TRADE_PHASE"].values:
        trade_date = player_df[player_df["TRADE_PHASE"] == "Post"].iloc[0]["GAME_DATE"]
        ax.axvline(trade_date, color="red", linestyle="--", label="Trade")

    ax.set_title(f"{player_name} – Key Stats Over Time")
    ax.set_xlabel("Game Date")
    ax.set_ylabel("Stat Value")
    ax.legend()
    plt.tight_layout()

    if save:
        os.makedirs("screenshots", exist_ok=True)
        fig.savefig(f"screenshots/{player_name.lower().replace(' ', '_')}_multi_stat_timeline.png")

    plt.show()

# -----------------------------------
# Run all visualizations
# -----------------------------------
if _name_ == "_main_":
    df = load_data()

    plot_ppg_change_bar(df, save=True)
    plot_bpm_boxplot(df, save=True)

    # Replace with your tested players
    plot_player_timeline(
        df,
        player_name="James Harden",
        stats=["PTS", "AST", "REB", "TA_BPM"],
        save=True
    )