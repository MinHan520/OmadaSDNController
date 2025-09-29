import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './login.css';

function Login() {
    // State to hold the values from the input fields
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [ipAddress, setIpAddress] = useState('10.30.31.199'); // Default IP
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    // useNavigate is a hook for programmatic navigation
    const navigate = useNavigate();

    // This function is called when the form is submitted
    const handleLogin = async (event) => {
        event.preventDefault(); // Prevent the default form submission
        setLoading(true);
        setError('');

        try {
            const response = await fetch('http://127.0.0.1:5000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ipAddress,
                    username,
                    password,
                }),
                credentials: 'include', // Important: This tells fetch to send cookies
            });

            const data = await response.json();

            if (!response.ok) {
                // If the server response is not OK (e.g., 401 Unauthorized)
                throw new Error(data.details || data.error || 'Login failed. Please check your credentials.');
            }

            // If login is successful
            alert('Successfully login into the TP-Link Omada Account.');
            // On success, the backend sets a session cookie. We can now navigate.
            navigate('/dashboard');

        } catch (err) {
            // If there's a network error or the server threw an error
            setError(err.message);
            alert(`Login Error: ${err.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <h1>Omada Controller Website</h1>
            <form onSubmit={handleLogin} className="login-form">
                <div className="form-group">
                    <label htmlFor="ipAddress">Controller IP Address</label>
                    <input
                        type="text"
                        id="ipAddress"
                        value={ipAddress}
                        onChange={(e) => setIpAddress(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Logging in...' : 'Login'}
                </button>
                {error && <p className="error-message">{error}</p>}
            </form>
        </div>
    );
}

export default Login;