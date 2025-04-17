// src/components/ServiceCard.jsx

import React from 'react';

const ServiceCard = ({ title, description, icon }) => (
    <div className="p-4 bg-white rounded shadow-md">
        <div className="text-3xl mb-2">{icon}</div>
        <h3 className="text-lg font-bold mb-1">{title}</h3>
        <p className="text-gray-600 text-sm">{description}</p>
    </div>
);

export default ServiceCard;