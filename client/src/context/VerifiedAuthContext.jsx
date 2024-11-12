import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useVerifiedAuth = () => useContext(AuthContext);

export const VerifiedAuthProvider = ({ children }) => {
    const [isVerified, setIsVerified] = useState(false);
    const [loading, setLoading] = useState(true);  // Track loading state

    // Check authentication status
    const checkAuth = async () => {
        try {
            const serverUrl = import.meta.env.VITE_SERVER_URL;  // Use your environment variable here

            // Use Axios to send the request
            const response = await axios.get(`${serverUrl}/api/authenticate/is-verified/`, {
                withCredentials: true,  // Ensure credentials are included in the request
            });

            if (response.status === 200) {
                setIsVerified(true);  // User is logged in
            } else {
                setIsVerified(false);  // User is not logged in
            }
        } catch (error) {
            setIsVerified(false);  // User is not logged in
        } finally {
            setLoading(false);  // Authentication check is done
        }
    };

    useEffect(() => {
        checkAuth();  // Check authentication status when app loads
    }, []);

    return (
        <AuthContext.Provider value={{ isVerified, checkAuth, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
