import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAdminAuth = () => useContext(AuthContext);

export const AdminAuthProvider = ({ children }) => {
    const [isAdmin, setIsAdmin] = useState(false);
    const [loading, setLoading] = useState(true);  // Track loading state

    // Check authentication status
    const checkAuth = async () => {
        try {
            const serverUrl = import.meta.env.VITE_SERVER_URL;  // Use your environment variable here

            // Use Axios to send the request
            const response = await axios.get(`${serverUrl}/api/authenticate/is-admin/`, {
                withCredentials: true,  // Ensure credentials are included in the request
            });

            if (response.status === 200) {
                setIsAdmin(true);  // User is logged in
            } else {
                setIsAdmin(false);  // User is not logged in
            }
        } catch (error) {
            setIsAdmin(false);  // User is not logged in
        } finally {
            setLoading(false);  // Authentication check is done
        }
    };

    useEffect(() => {
        checkAuth();  // Check authentication status when app loads
    }, []);

    return (
        <AuthContext.Provider value={{ isAdmin, checkAuth, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
