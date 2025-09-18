import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import './sidebar.css'; // We'll create this new CSS file

function Sidebar({ isRetracted, toggleSidebar }) {
    return (
        <aside className={`sidebar ${isRetracted ? 'retracted' : ''}`}>
            <div className="sidebar-header">
                <button className="hamburger-button" onClick={toggleSidebar}>
                    ☰
                </button>
                <h3>Omada Controller</h3>
            </div>
            <nav className="sidebar-nav">
                <ul>
                    {/* Dashboard Link */}
                    <li>
                        <NavLink to="/dashboard" className={({ isActive }) => isActive ? "active-link" : ""}>
                            Dashboard
                        </NavLink>
                    </li>

                    {/* User Management Dropdown */}
                    <li className="dropdown">
                        <span className="dropdown-toggle">Users</span>
                        <ul className="dropdown-menu">
                            <li><NavLink to="/users">User List</NavLink></li>
                            <li><NavLink to="/roles">Role List</NavLink></li>
                            {/* Add links to create/modify users later */}
                        </ul>
                    </li>

                    {/* Placeholder for future links */}
                    <li className="dropdown">
                        <span className="dropdown-toggle">Network (TBD)</span>
                         <ul className="dropdown-menu">
                            <li><Link to="#">Routing</Link></li>
                            <li><Link to="#">Devices</Link></li>
                        </ul>
                    </li>
                </ul>
            </nav>
        </aside>
    );
}

export default Sidebar;