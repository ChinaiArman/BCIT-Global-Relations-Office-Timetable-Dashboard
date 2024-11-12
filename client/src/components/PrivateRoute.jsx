import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';

// A wrapper component that protects routes
const PrivateRoute = ({ children }) => {
    const { isAuthenticated, loading } = useAuth();

    if (loading) {
        // You can return a loading spinner or some placeholder
        return <div>Loading...</div>;
    }

    return isAuthenticated ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
