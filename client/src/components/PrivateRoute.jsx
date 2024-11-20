import { Navigate } from 'react-router-dom';
import { useUnverifiedAuth } from '../context/UnverifiedAuthContext.jsx';
import { useVerifiedAuth } from '../context/VerifiedAuthContext.jsx';
import { useAdminAuth } from '../context/AdminContext.jsx';

const PrivateRoute = ({ children, role }) => {
    const { isUnverified, loading: loadingUnverified } = useUnverifiedAuth();
    const { isVerified, loading: loadingVerified } = useVerifiedAuth();
    const { isAdmin, loading: loadingAdmin } = useAdminAuth();

    const loading = loadingUnverified || loadingVerified || loadingAdmin;

    if (loading) {
        return <div>Loading...</div>;
    }

    if (role === 'admin' && isAdmin) return children;
    if (role === 'verified' && (isVerified || isAdmin)) return children;
    if (role === 'unverified' && isUnverified) return children;

    // Redirect based on role type
    return <Navigate to="/login" />;
};

export default PrivateRoute;
