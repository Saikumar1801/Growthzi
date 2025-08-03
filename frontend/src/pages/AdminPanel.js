import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import * as adminApi from '../api/admin';
import Loader from '../components/Loader';

const AdminPanel = () => {
    const [roles, setRoles] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [userId, setUserId] = useState('');
    const [selectedRole, setSelectedRole] = useState('');

    useEffect(() => {
        const fetchRoles = async () => {
            try {
                const response = await adminApi.getAllRoles();
                setRoles(response.data);
                if (response.data.length > 0) {
                    setSelectedRole(response.data[0].name);
                }
            } catch (error) {
                toast.error("Failed to load roles.");
            } finally {
                setIsLoading(false);
            }
        };
        fetchRoles();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!userId || !selectedRole) {
            toast.error("Please provide a User ID and select a role.");
            return;
        }

        try {
            await toast.promise(
                adminApi.assignRoleToUser(userId, selectedRole),
                {
                    loading: 'Assigning role...',
                    success: `Successfully assigned role '${selectedRole}' to user.`,
                    error: (err) => err.response?.data?.error || "Failed to assign role."
                }
            );
            setUserId('');
        } catch (error) {
            // Toast handles the message
        }
    };
    
    if (isLoading) return <Loader />;

    return (
        <>
            <div className="page-header">
                <h1>Admin Panel</h1>
            </div>
            <div className="form-container" style={{margin: '0 auto'}}>
                <h2>Assign Role to User</h2>
                <p>To build a full user list, a `GET /api/admin/users` endpoint would be required.</p>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="userId">User ID</label>
                        <input
                            id="userId"
                            type="text"
                            placeholder="Enter the user's Object ID"
                            value={userId}
                            onChange={(e) => setUserId(e.target.value)}
                            required
                        />
                    </div>
                     <div className="form-group">
                        <label htmlFor="role">Role</label>
                        <select
                            id="role"
                            value={selectedRole}
                            onChange={(e) => setSelectedRole(e.target.value)}
                            required
                        >
                            {roles.map(role => (
                                <option key={role._id} value={role.name}>{role.name}</option>
                            ))}
                        </select>
                    </div>
                    <button type="submit" className="btn btn-primary btn-block">Assign Role</button>
                </form>
            </div>
        </>
    );
};

export default AdminPanel; 
