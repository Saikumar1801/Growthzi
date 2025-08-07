import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import * as adminApi from '../api/admin';
import useAuth from '../hooks/useAuth'; // Import useAuth to get the current user
import Loader from '../components/Loader';
import './AdminPanel.css';

const AdminPanel = () => {
    const [users, setUsers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const { user: currentUser } = useAuth(); // Get the currently logged-in admin user

    const fetchUsers = async () => {
        setIsLoading(true);
        try {
            const response = await adminApi.getAllUsers();
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

    const handleChangeRole = async (userId, userEmail, newRole) => {
        const action = newRole === 'Admin' ? 'Promoting' : 'Changing role for';
        const toastId = toast.loading(`${action} ${userEmail} to ${newRole}...`);
        
        try {
            await adminApi.assignRoleToUser(userId, newRole);
            toast.success(`${userEmail}'s role is now ${newRole}!`, { id: toastId });
            // Refresh the user list to show the new role
            fetchUsers();
        } catch (error) {
            toast.error(error.response?.data?.error || "Action failed.", { id: toastId });
        }
    };
    
    if (isLoading) return <Loader />;

    return (
        <>
            <div className="page-header">
                <h1>Admin Panel - User Management</h1>
            </div>
            <div className="admin-table-container">
                <p>Manage user roles below. Changes take effect immediately.</p>
                <table className="user-table">
                    <thead>
                        <tr>
                            <th>Email</th>
                            <th>Current Role</th>
                            <th>Date Joined</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(user => (
                            <tr key={user._id}>
                                <td>
                                    {user.email}
                                    {user._id === currentUser.id && <span className="you-badge">(You)</span>}
                                </td>
                                <td>
                                    <span className={`role-badge role-${user.role?.toLowerCase()}`}>
                                        {user.role}
                                    </span>
                                </td>
                                <td>{new Date(user.created_at).toLocaleDateString()}</td>
                                <td className="action-cell">
                                    {/* Prevent an admin from changing their own role */}
                                    {user._id === currentUser.id ? (
                                        <span className="action-text">Cannot change own role</span>
                                    ) : (
                                        <div className="action-buttons">
                                            {user.role === 'Viewer' && (
                                                <button 
                                                    className="btn btn-primary"
                                                    onClick={() => handleChangeRole(user._id, user.email, 'Editor')}
                                                >
                                                    Promote to Editor
                                                </button>
                                            )}
                                            {user.role === 'Editor' && (
                                                <>
                                                    <button 
                                                        className="btn btn-success"
                                                        onClick={() => handleChangeRole(user._id, user.email, 'Admin')}
                                                    >
                                                        Promote to Admin
                                                    </button>
                                                    <button 
                                                        className="btn btn-secondary"
                                                        onClick={() => handleChangeRole(user._id, user.email, 'Viewer')}
                                                    >
                                                        Demote to Viewer
                                                    </button>
                                                </>
                                            )}
                                            {user.role === 'Admin' && (
                                                 <button 
                                                    className="btn btn-danger"
                                                    onClick={() => handleChangeRole(user._id, user.email, 'Editor')}
                                                >
                                                    Demote to Editor
                                                </button>
                                            )}
                                        </div>
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