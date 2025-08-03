 
import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
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
                    const decoded = jwtDecode(token);
                    if (decoded.exp * 1000 > Date.now()) {
                        const role = await authApi.fetchUserRole();
                        setUser({ id: decoded.user_id, role });
                    } else {
                        authApi.logout(); // Token expired
                    }
                } catch (error) {
                    console.error("Token validation failed", error);
                    authApi.logout();
                }
            }
            setLoading(false);
        };
        initializeAuth();
    }, []);

    const login = async (email, password) => {
        const data = await authApi.login(email, password);
        const decoded = jwtDecode(data.token);
        const role = await authApi.fetchUserRole();
        setUser({ id: decoded.user_id, role });
    };

    const signup = async (email, password) => {
        await authApi.signup(email, password);
        // After signup, log the user in automatically
        await login(email, password);
    };

    const logout = () => {
        authApi.logout();
        setUser(null);
    };
    
    // While the context is initializing, show a loader
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