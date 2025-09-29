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
          {/* Public routes (no sidebar) */}
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Navigate to="/login" />} />

          {/* Private routes wrapped by the Layout component */}
          <Route element={<Layout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/userlist" element={<UserList />} />
          </Route>

          <Route path="*" element={<div>404 - Page Not Found</div>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
