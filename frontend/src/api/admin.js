import apiClient from './axiosConfig';

const API_URL = '/api/admin/';

// --- NEW FUNCTION ---
export const getAllUsers = () => {
    return apiClient.get(`${API_URL}users`);
};
// --------------------

export const getAllRoles = () => {
    return apiClient.get(`${API_URL}roles`);
};

export const assignRoleToUser = (userId, roleName) => {
    return apiClient.put(`${API_URL}users/${userId}/assign-role`, { role_name: roleName });
};