// src/components/StatCard.jsx
import React from 'react';

const StatCard = ({ label, value, highlight = false }) => (
    <div className={`p-4 rounded shadow-md ${highlight ? 'bg-yellow-100' : 'bg-white'}`}>
        <p className="text-sm text-gray-500">{label}</p>
        <p className="text-xl font-semibold">{value}</p>
    </div>
);

export default StatCard;
