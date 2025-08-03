 
import axios from 'axios';

const API_URL = '/api/auth';

const axiosInstance = axios.create({
    baseURL: API_URL,
});

export const signup = (email, password) => {
    return axiosInstance.post('/signup', { email, password });
};

export const login = async (email, password) => {
    const response = await axiosInstance.post('/login', { email, password });
    if (response.data.token) {
        localStorage.setItem('token', response.data.token);
    }
    return response.data;
};

export const logout = () => {
    localStorage.removeItem('token');
};

// This function is a placeholder for a dedicated endpoint
// that would ideally return the current user's full profile including their role.
// For now, we fetch all roles, and if it succeeds, we know the user is an Admin.
// In AuthContext, we'll use this to determine the user's role after login.
export const fetchUserRole = async () => {
    try {
        await axios.get('/api/admin/roles', {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        return 'Admin'; // Success means user has 'roles:manage' permission
    } catch (error) {
        if (error.response && error.response.status === 403) {
            // This is not a foolproof way to determine Editor vs Viewer,
            // but for this app, we assume non-admins are Editors as Viewers can't log in to a dashboard.
            return 'Editor';
        }
        // If the token is invalid or another error occurs, role is unknown.
        return null;
    }
};