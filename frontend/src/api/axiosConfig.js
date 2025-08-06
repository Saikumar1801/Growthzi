import axios from 'axios';

// Get the backend URL from the environment variable.
// In development, this will be undefined, so we fall back to the proxy.
// In production (On-Render), it will be set to the backend's live URL.
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Add a request interceptor to include the token on every request.
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;