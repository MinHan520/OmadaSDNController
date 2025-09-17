import React from 'react';
import { Link } from 'react-router-dom';
import './dashboard.css';

function Dashboard() {
    return (
        <div className="dashboard-container">
            <aside className="sidebar">
                <div className="sidebar-header">
                    <h3>Omada Controller</h3>
                </div>
                <nav className="sidebar-nav">
                    <ul>
                        <li><Link to="/users">Users</Link></li>
                        {/* These are placeholders for future pages */}
                        <li><Link to="/dashboard">Routing (TBD)</Link></li>
                        <li><Link to="/dashboard">Devices (TBD)</Link></li>
                    </ul>
                </nav>
            </aside>
            <main className="main-content">
                <h1>Welcome to Your Dashboard</h1>
                <p>Select an option from the navigation menu on the left to manage your network.</p>
            </main>
        </div>
    );
}

export default Dashboard;