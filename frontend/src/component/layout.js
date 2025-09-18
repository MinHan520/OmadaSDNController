import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './sidebar/sidebar.js';
import './Layout.css';

function Layout() {
    const [sidebarRetracted, setSidebarRetracted] = useState(false);

    const toggleSidebar = () => {
        setSidebarRetracted(!sidebarRetracted);
    };

    return (
        <div className={`app-container ${sidebarRetracted ? 'sidebar-retracted' : ''}`}>
            <Sidebar isRetracted={sidebarRetracted} toggleSidebar={toggleSidebar} />
            <main className="main-content">
                {/* The Outlet component renders the matched child route component */}
                <Outlet />
            </main>
        </div>
    );
}

export default Layout;