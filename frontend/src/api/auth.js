import apiClient from './axiosConfig';

// Registers a new user
export const signup = (email, password) => {
    return apiClient.post('/api/auth/signup', { email, password });
};

// Logs in a user
export const login = async (email, password) => {
    const response = await apiClient.post('/api/auth/login', { email, password });
    if (response.data.token) {
        localStorage.setItem('token', response.data.token);
    }
    return response.data;
};

// Clears the token from local storage
export const logout = () => {
    localStorage.removeItem('token');
};

// --- NEW FUNCTION: Fetches the current user's profile from the backend ---
// This is more reliable than the old method of trying an admin-only action.
export const getMe = () => {
    return apiClient.get('/api/auth/me');
};
// ----------------------------------------------------------------------