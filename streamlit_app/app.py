import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="TTP Trade Dashboard", layout="wide")
sns.set(style="whitegrid")

# Load data
df = pd.read_csv("data/processed/with_bpm.csv")
df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])

# Try to get SEASON and POSITION if available
if 'SEASON' not in df.columns:
    df['SEASON'] = df['GAME_DATE'].dt.year
if 'POSITION' not in df.columns:
    df['POSITION'] = 'Unknown'  # Placeholder if missing

# Sidebar filters
st.sidebar.title("Filters")

# Player selection
player_names = df["PLAYER_NAME"].unique()
selected_player = st.sidebar.selectbox("Select Player", sorted(player_names))

# Team filter
teams = df["TEAM_ABBREVIATION"].unique()
selected_teams = st.sidebar.multiselect("Filter by Team(s)", sorted(teams), default=teams)

# Season filter
seasons = sorted(df["SEASON"].unique())
selected_seasons = st.sidebar.multiselect("Filter by Season(s)", seasons, default=seasons)

# Position filter
positions = df["POSITION"].unique()
selected_positions = st.sidebar.multiselect("Filter by Position(s)", sorted(positions), default=positions)

# Filter data
filtered_df = df[
    (df["TEAM_ABBREVIATION"].isin(selected_teams)) &
    (df["SEASON"].isin(selected_seasons)) &
    (df["POSITION"].isin(selected_positions))
]

# Filter player-specific data
player_df = filtered_df[filtered_df["PLAYER_NAME"] == selected_player].sort_values(by="GAME_DATE")

# Header
st.title("TTP – Trade Transition Dashboard")
st.markdown("Analyze NBA player performance before and after trades")

# --- Line plot of PTS ---
st.subheader(f"{selected_player} – Game-by-Game Points")
fig1, ax1 = plt.subplots()
ax1.plot(player_df["GAME_DATE"], player_df["PTS"], marker="o", label="PTS")
if "Post" in player_df["TRADE_PHASE"].values:
    trade_date = player_df[player_df["TRADE_PHASE"] == "Post"].iloc[0]["GAME_DATE"]
    ax1.axvline(trade_date, color="red", linestyle="--", label="Trade")
ax1.set_xlabel("Game Date")
ax1.set_ylabel("Points")
ax1.legend()
st.pyplot(fig1)

# --- Stat deltas ---
st.subheader("Average Stat Changes Pre vs Post Trade")
avg_stats = filtered_df.groupby(["PLAYER_NAME", "TRADE_PHASE"])[["PTS", "AST", "REB", "TA_BPM"]].mean().reset_index()
pivoted = avg_stats.pivot(index="PLAYER_NAME", columns="TRADE_PHASE")
pivoted.columns = ['_'.join(col).strip() for col in pivoted.columns.values]
pivoted["PTS_DIFF"] = pivoted["PTS_Post"] - pivoted["PTS_Pre"]
pivoted["AST_DIFF"] = pivoted["AST_Post"] - pivoted["AST_Pre"]
pivoted["BPM_DIFF"] = pivoted["TA_BPM_Post"] - pivoted["TA_BPM_Pre"]
pivoted = pivoted.dropna()

top_drops = pivoted.nsmallest(10, "PTS_DIFF")

fig2, ax2 = plt.subplots()
top_drops["PTS_DIFF"].plot(kind="barh", ax=ax2, color="tomato")
ax2.set_title("Top 10 Players – Drop in PPG After Trade")
ax2.set_xlabel("Δ PPG")
st.pyplot(fig2)

# --- BPM distribution ---
st.subheader("TA-BPM Distribution Before vs After Trade")
fig3, ax3 = plt.subplots()
sns.boxplot(data=filtered_df, x="TRADE_PHASE", y="TA_BPM", ax=ax3)
ax3.set_title("TA-BPM Pre vs Post Trade")
st.pyplot(fig3)