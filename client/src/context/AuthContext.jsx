import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);  // Track loading state

    // Check authentication status
    const checkAuth = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/authenticate/get-user-info/', {
                credentials: 'include',  // Ensure credentials are included in the request
            });

            if (response.ok) {
                setIsAuthenticated(true);  // User is logged in
            } else {
                setIsAuthenticated(false);  // User is not logged in
            }
        } catch (error) {
            console.error("Error checking authentication:", error);
            setIsAuthenticated(false);  // User is not logged in
        } finally {
            setLoading(false);  // Authentication check is done
        }
    };

    useEffect(() => {
        checkAuth();  // Check authentication status when app loads
    }, []);

    return (
        <AuthContext.Provider value={{ isAuthenticated, checkAuth, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
