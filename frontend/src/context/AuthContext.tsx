// src/contexts/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../utils/api';

interface AuthContextType {
    isAuthenticated: boolean;
    loginLocal: (email: string, password: string) => Promise<void>;
    register: (email: string, password: string) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        // Check for existing token on mount
        const token = localStorage.getItem('token');
        setIsAuthenticated(!!token);
    }, []);

    const loginLocal = async (email: string, password: string) => {
        try {
            const response = await api.post('/api/auth/login', {
                email,
                password,
            });

            const data = response.data;
            localStorage.setItem('token', data.token);
            setIsAuthenticated(true);
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'Login failed');
        }
    };

    const register = async (email: string, password: string) => {
        try {
            const response = await api.post('/api/auth/register', {
                email,
                password,
                confirmPassword: password,
            });

            const data = response.data;
            localStorage.setItem('token', data.token);
            setIsAuthenticated(true);
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'Registration failed');
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, loginLocal, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
