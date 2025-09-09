import React, { useState, useEffect } from 'react';

function UserList() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data from your Flask backend
    fetch('http://127.0.0.1:5000/api/users')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.errorCode === 0) {
          setUsers(data.result.data);
        } else {
          setError(data.error || 'Failed to fetch users');
        }
        setLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setLoading(false);
      });
  }, []); // The empty array means this effect runs once on component mount

  if (loading) return <div>Loading users...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>Omada Controller Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name} ({user.email}) - Role: {user.roleName}</li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;