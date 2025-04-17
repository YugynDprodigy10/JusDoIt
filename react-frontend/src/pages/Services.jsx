// src/pages/Services.jsx

import React from 'react';
import ServiceCard from '../components/ServiceCard';

const services = [
    {
        title: "Mentorship",
        description: "Get matched with a veteran player who’s experienced trade transitions.",
        icon: "🤝"
    },
    {
        title: "Relocation Aid",
        description: "Support for moving, housing, and family adjustment.",
        icon: "🚚"
    },
    {
        title: "Career Counseling",
        description: "Plan your future beyond your current team or season.",
        icon: "📈"
    },
    {
        title: "Mental Health Support",
        description: "Access licensed therapists and performance coaches.",
        icon: "🧠"
    },
    {
        title: "Contract & Legal Help",
        description: "Understand your post-trade rights and renegotiate contracts.",
        icon: "📄"
    },
    {
        title: "Lifestyle Optimization",
        description: "Get customized nutrition, sleep, and training support.",
        icon: "🏋️"
    }
];

const Services = () => (
    <div className="p-8">
        <h2 className="text-2xl font-bold mb-6">Support Services</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {services.map((service, i) => (
                <ServiceCard key={i} {...service} />
            ))}
        </div>
    </div>
);

export default Services;
