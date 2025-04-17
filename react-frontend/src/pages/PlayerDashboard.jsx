import React, { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const PlayerDashboard = () => {
    const [filters, setFilters] = useState({ players: [], teams: [], positions: [], seasons: [] });
    const [selectedPlayer, setSelectedPlayer] = useState("James Harden");
    const [selectedTeam, setSelectedTeam] = useState("");
    const [selectedPosition, setSelectedPosition] = useState("");
    const [selectedSeason, setSelectedSeason] = useState("");
    const [playerData, setPlayerData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("http://localhost:5000/api/filters")
            .then((res) => res.json())
            .then((data) => setFilters(data))
            .catch((err) => console.error("Failed to fetch filters", err));
    }, []);

    useEffect(() => {
        if (!selectedPlayer) return;
        setLoading(true);
        setError(null);
        const url = `http://localhost:5000/api/player/${encodeURIComponent(selectedPlayer)}?team=${selectedTeam}&position=${selectedPosition}&season=${selectedSeason}`;

        fetch(url)
            .then((res) => {
                if (!res.ok) throw new Error("No data found");
                return res.json();
            })
            .then((data) => setPlayerData(data))
            .catch((err) => setError(err.message))
            .finally(() => setLoading(false));
    }, [selectedPlayer, selectedTeam, selectedPosition, selectedSeason]);

    const statChartData = playerData
        ? [
            {
                name: "PPG",
                Pre: playerData.ppg_pre,
                Post: playerData.ppg_post,
            },
            {
                name: "AST",
                Pre: playerData.ast_pre,
                Post: playerData.ast_post,
            },
            {
                name: "TA-BPM",
                Pre: playerData.ta_bpm_pre,
                Post: playerData.ta_bpm_post,
            },
        ]
        : [];

    return (
        <div style={{ padding: "20px" }}>
            <h2>Trade Impact Dashboard</h2>
            <div style={{ marginBottom: "15px" }}>
                <label>
                    Player
                    <select value={selectedPlayer} onChange={(e) => setSelectedPlayer(e.target.value)}>
                        {filters.players.map((p) => (
                            <option key={p} value={p}>{p}</option>
                        ))}
                    </select>
                </label>
                <br />
                <label>
                    Team
                    <select value={selectedTeam} onChange={(e) => setSelectedTeam(e.target.value)}>
                        <option value="">All</option>
                        {filters.teams.map((t) => (
                            <option key={t} value={t}>{t}</option>
                        ))}
                    </select>
                </label>
                <br />
                <label>
                    Position
                    <select value={selectedPosition} onChange={(e) => setSelectedPosition(e.target.value)}>
                        <option value="">All</option>
                        {filters.positions.map((pos) => (
                            <option key={pos} value={pos}>{pos}</option>
                        ))}
                    </select>
                </label>
                <br />
                <label>
                    Season
                    <select value={selectedSeason} onChange={(e) => setSelectedSeason(e.target.value)}>
                        <option value="">All</option>
                        {filters.seasons.map((s) => (
                            <option key={s} value={s}>{s}</option>
                        ))}
                    </select>
                </label>
            </div>

            {loading && <p>Loading player data...</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}

            {playerData && (
                <>
                    <h3>{playerData.name} - Stat Comparison</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={statChartData} margin={{ top: 10, right: 30, left: 0, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="Pre" fill="#8884d8" />
                            <Bar dataKey="Post" fill="#82ca9d" />
                        </BarChart>
                    </ResponsiveContainer>
                </>
            )}
        </div>
    );
};

export default PlayerDashboard;
