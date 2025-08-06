import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import * as adminApi from '../api/admin';
import Loader from '../components/Loader';
import './AdminPanel.css'; // We'll create this for styling

const AdminPanel = () => {
    const [users, setUsers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    const fetchUsers = async () => {
        try {
            const response = await adminApi.getAllUsers();
            // Sort users by creation date, newest first
            const sortedUsers = response.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            setUsers(sortedUsers);
        } catch (error) {
            toast.error("Failed to load users.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    const handlePromote = async (userId, userEmail) => {
        const toastId = toast.loading(`Promoting ${userEmail} to Editor...`);
        try {
            await adminApi.assignRoleToUser(userId, 'Editor');
            toast.success(`${userEmail} is now an Editor!`, { id: toastId });
            // Refresh the user list to show the new role
            fetchUsers();
        } catch (error) {
            toast.error(error.response?.data?.error || "Promotion failed.", { id: toastId });
        }
    };
    
    if (isLoading) return <Loader />;

    return (
        <>
            <div className="page-header">
                <h1>Admin Panel - User Management</h1>
            </div>
            <div className="admin-table-container">
                <p>New users sign up as 'Viewers'. Promote them to 'Editors' to allow them to create and manage websites.</p>
                <table className="user-table">
                    <thead>
                        <tr>
                            <th>Email</th>
                            <th>Current Role</th>
                            <th>Date Joined</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(user => (
                            <tr key={user._id}>
                                <td>{user.email}</td>
                                <td>
                                    <span className={`role-badge role-${user.role?.toLowerCase()}`}>
                                        {user.role}
                                    </span>
                                </td>
                                <td>{new Date(user.created_at).toLocaleDateString()}</td>
                                <td>
                                    {user.role === 'Viewer' && (
                                        <button 
                                            className="btn btn-primary"
                                            onClick={() => handlePromote(user._id, user.email)}
                                        >
                                            Promote to Editor
                                        </button>
                                    )}
                                    {user.role === 'Editor' && (
                                        <span className="action-text">Can create content</span>
                                    )}
                                    {user.role === 'Admin' && (
                                        <span className="action-text">Full access</span>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    );
};

export default AdminPanel;