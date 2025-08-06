import React, { createContext, useState, useEffect } from 'react';
import * as authApi from '../api/auth';
import Loader from '../components/Loader';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const initializeAuth = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    // --- CHANGE: Use the new /me endpoint for reliability ---
                    const response = await authApi.getMe();
                    // The backend now tells us the role directly.
                    setUser({ id: response.data.id, role: response.data.role });
                    // ----------------------------------------------------
                } catch (error) {
                    console.error("Token validation failed or user not found", error);
                    authApi.logout(); // Token is invalid, log them out.
                }
            }
            setLoading(false);
        };
        initializeAuth();
    }, []);

    const login = async (email, password) => {
        await authApi.login(email, password); // This sets the token in localStorage
        // --- CHANGE: Use the new /me endpoint after login ---
        const response = await authApi.getMe();
        setUser({ id: response.data.id, role: response.data.role });
        // -------------------------------------------------
    };

    const signup = async (email, password) => {
        await authApi.signup(email, password);
        // After signup, automatically log the user in to get their token and profile.
        await login(email, password);
    };

    const logout = () => {
        authApi.logout();
        setUser(null);
    };
    
    if (loading) {
        return <Loader />;
    }

    return (
        <AuthContext.Provider value={{ user, login, signup, logout, isAuthenticated: !!user }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthContext;