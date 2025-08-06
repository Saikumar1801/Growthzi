import apiClient from './axiosConfig'; // Import the centralized client

const API_URL = '/api/websites/'; // The base path for all website-related endpoints

// Calls the AI to generate content and create a new website document.
export const generateWebsite = (business_type, industry) => {
    return apiClient.post(`${API_URL}generate`, { business_type, industry });
};

// Retrieves a list of websites (Admins see all, others see their own).
export const getWebsites = () => {
    return apiClient.get(API_URL);
};

// Retrieves the data for a single website by its ID.
export const getWebsiteById = (id) => {
    return apiClient.get(`${API_URL}${id}`);
};

// Updates the content of a specific website.
export const updateWebsite = (id, content) => {
    return apiClient.put(`${API_URL}${id}`, { content });
};

// Deletes a specific website.
export const deleteWebsite = (id) => {
    return apiClient.delete(`${API_URL}${id}`);
};