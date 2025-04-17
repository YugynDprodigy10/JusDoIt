from flask import Flask, jsonify, send_from_directory, request
import os
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_PATH = "data/processed/with_bpm.csv"
CHARTS_DIR = "screenshots"

# Load data once to reduce I/O overhead
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
    df["SEASON"] = df["GAME_DATE"].dt.year.astype(str)
    return df

# Safe rounding that handles NaN
def safe_round(val):
    return round(val, 1) if pd.notna(val) else None

@app.route("/api/player/<player_name>")
def get_player_data(player_name):
    team = request.args.get("team")
    position = request.args.get("position")
    season = request.args.get("season")

    df = load_data()
    player_df = df[df["PLAYER_NAME"].str.lower() == player_name.lower()]

    if team and team.strip():
        player_df = player_df[player_df["TEAM_ABBREVIATION"] == team]
    if position and position.strip() and "POSITION" in player_df.columns:
        player_df = player_df[player_df["POSITION"] == position]
    if season and season.strip():
        player_df = player_df[player_df["SEASON"] == season]

    if player_df.empty:
        return jsonify({"error": "Player not found"}), 404

    pre = player_df[player_df["TRADE_PHASE"] == "Pre"].mean(numeric_only=True)
    post = player_df[player_df["TRADE_PHASE"] == "Post"].mean(numeric_only=True)

    return jsonify({
        "name": player_name,
        "ppg_pre": safe_round(pre.get("PTS")),
        "ppg_post": safe_round(post.get("PTS")),
        "ast_pre": safe_round(pre.get("AST")),
        "ast_post": safe_round(post.get("AST")),
        "ta_bpm_pre": safe_round(pre.get("TA_BPM")),
        "ta_bpm_post": safe_round(post.get("TA_BPM")),
        "table": player_df.to_dict(orient="records")
    })

@app.route("/api/players")
def get_player_list():
    df = load_data()
    player_names = sorted(df["PLAYER_NAME"].unique().tolist())
    return jsonify(player_names)

@app.route("/api/filters")
def get_filters():
    df = load_data()
    filters = {
        "players": sorted(df["PLAYER_NAME"].unique().tolist()),
        "teams": sorted(df["TEAM_ABBREVIATION"].unique().tolist()),
        "positions": sorted(df["POSITION"].dropna().unique().tolist()) if "POSITION" in df.columns else [],
        "seasons": sorted(df["SEASON"].dropna().unique().tolist())
    }
    return jsonify(filters)

@app.route("/charts/<filename>")
def get_chart(filename):
    return send_from_directory(CHARTS_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
