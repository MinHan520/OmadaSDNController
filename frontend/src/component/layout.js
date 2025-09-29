import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../sidebar/sidebar.js';
import './layout.css';

function Layout() {
    const [sidebarRetracted, setSidebarRetracted] = useState(false);

    const toggleSidebar = () => {
        setSidebarRetracted(!sidebarRetracted);
    };

    return (
        <div className={`dashboard-container ${sidebarRetracted ? 'sidebar-retracted' : ''}`}>
            <button className="hamburger-button" onClick={toggleSidebar}>
                {sidebarRetracted ? '☰' : '❮'}
            </button>
            <Sidebar isRetracted={sidebarRetracted} />
            <main className="main-content">
                {/* The Outlet component renders the matched child route component */}
                <Outlet />
            </main>
        </div>
    );
}

export default Layout;