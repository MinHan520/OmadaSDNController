import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import UserList from './UserList';
import Login from './login/login.js';
import Dashboard from './dashboard/dashboard.js'; 
import Layout from './component/layout.js';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Default route redirects to /login */}
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Navigate to="/login" />} />
          <Route element={<Layout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/users" element={<UserList />} />
          </Route>
          <Route path="*" element={<div>404 - Page Not Ground</div>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
