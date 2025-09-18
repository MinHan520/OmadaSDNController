import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './dashboard.css';

function Dashboard() {
    const [sidebarRetracted, setSidebarRetracted] = useState(false);
    const toggleSidebar = () => {
        setSidebarRetracted(!sidebarRetracted);
    };

    return (
        //<div className="dashboard-container"> {sidebarRetracted ? '>' : '<'}

            <main className="main-content">
                <h1>Welcome to Your Dashboard</h1>
                <p>Select an option from the navigation menu on the left to manage your network.</p>
            </main>
    );
}

export default Dashboard;