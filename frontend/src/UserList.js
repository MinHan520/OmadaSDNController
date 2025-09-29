import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserList.css'; // We'll create this file next

function UserList() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [totalUsers, setTotalUsers] = useState(0);
    const navigate = useNavigate();
    const pageSize = 10;

    useEffect(() => {
        const fetchUsers = async () => {
            setLoading(true);
            try {
                // The 'credentials: include' option is crucial for sending cookies
                // to the backend for session-based authentication.
                const response = await fetch(`/api/users?page=${currentPage}&pageSize=${pageSize}`, {
                    credentials: 'include',
                });

                if (response.status === 401) {
                    // If not authenticated, redirect to login
                    navigate('/login');
                    return;
                }

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();

                if (data.errorCode === 0) {
                    // The actual user data is in result.data
                    setUsers(data.result.data || []);
                    setTotalUsers(data.result.totalRows || 0);
                    setTotalPages(Math.ceil((data.result.totalRows || 0) / pageSize));
                } else {
                    throw new Error(data.error || 'Failed to fetch users');
                }
            } catch (e) {
                setError(e.message);
            } finally {
                setLoading(false);
            }
        };

        fetchUsers();
    }, [currentPage, navigate]); // Refetch users when currentPage changes

    if (loading) return <div>Loading users...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="user-list-container">
            <h1>User Management</h1>
            <p>Showing {users.length} of {totalUsers} users registered in the Omada Controller.</p>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Role</th>
                    </tr>
                </thead>
                <tbody>
                    {users.length > 0 ? users.map(user => (
                        <tr key={user.id}>
                            <td>{user.name}</td>
                            <td>{user.email || 'N/A'}</td>
                            <td>{user.roleName}</td>
                        </tr>
                    )) : ( <tr><td colSpan="3">No users found.</td></tr> )}
                </tbody>
            </table>
            <div className="pagination-controls">
                <button onClick={() => setCurrentPage(p => p - 1)} disabled={currentPage === 1}>
                    Previous
                </button>
                <span>Page {currentPage} of {totalPages}</span>
                <button onClick={() => setCurrentPage(p => p + 1)} disabled={currentPage >= totalPages}>
                    Next
                </button>
            </div>
        </div>
    );
}

export default UserList;