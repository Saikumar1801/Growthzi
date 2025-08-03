 
import axios from 'axios';

const API_URL = '/api/websites/';

const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return token ? { Authorization: `Bearer ${token}` } : {};
};

export const generateWebsite = (business_type, industry) => {
    return axios.post(`${API_URL}/generate`, { business_type, industry }, { headers: getAuthHeaders() });
};

export const getWebsites = () => {
    return axios.get(API_URL, { headers: getAuthHeaders() });
};

export const getWebsiteById = (id) => {
    return axios.get(`${API_URL}/${id}`, { headers: getAuthHeaders() });
};

export const updateWebsite = (id, content) => {
    return axios.put(`${API_URL}/${id}`, { content }, { headers: getAuthHeaders() });
};

export const deleteWebsite = (id) => {
    return axios.delete(`${API_URL}/${id}`, { headers: getAuthHeaders() });
};