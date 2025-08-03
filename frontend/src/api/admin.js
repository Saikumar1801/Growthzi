import axios from 'axios';

const API_URL = '/api/admin/';

const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return token ? { Authorization: `Bearer ${token}` } : {};
};

export const getAllRoles = () => {
    return axios.get(`${API_URL}/roles`, { headers: getAuthHeaders() });
};

export const assignRoleToUser = (userId, roleName) => {
    return axios.put(`${API_URL}/users/${userId}/assign-role`, { role_name: roleName }, { headers: getAuthHeaders() });
}; 
