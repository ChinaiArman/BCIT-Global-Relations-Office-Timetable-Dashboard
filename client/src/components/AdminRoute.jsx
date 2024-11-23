// components/AdminRoute.jsx
import { useState, useEffect } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const AdminRoute = ({ children }) => {
    const [isAdmin, setIsAdmin] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const location = useLocation();

    useEffect(() => {
        const checkAdminStatus = async () => {
            try {
                const serverUrl = import.meta.env.VITE_SERVER_URL;
                await axios.get(`${serverUrl}/api/authenticate/is-admin/`, {
                    withCredentials: true
                });
                setIsAdmin(true);
            } catch (error) {
                setIsAdmin(false);
            } finally {
                setIsLoading(false);
            }
        };

        checkAdminStatus();
    }, []);

    if (isLoading) {
        // You can replace this with a loading spinner
        return <div>Loading...</div>;
    }

    if (!isAdmin) {
        // Redirect to AdminOnly page with the attempted path stored in state
        return <Navigate to="/admin-only" state={{ from: location }} replace />;
    }

    return children;
};

export default AdminRoute;