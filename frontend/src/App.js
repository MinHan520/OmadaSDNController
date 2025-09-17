import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import UserList from './UserList';
import Login from './login/login.js';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Default route redirects to /login */}
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/users" element={<UserList />} />
        </Routes>
      </div>

    </Router>
  );
}

export default App;
