 
import { Navigate, useLocation } from 'react-router-dom';
import useAuth from '../hooks/useAuth';
import toast from 'react-hot-toast';

const PrivateRoute = ({ children, roles }) => {
    const { isAuthenticated, user } = useAuth();
    const location = useLocation();

    if (!isAuthenticated) {
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    // If specific roles are required, check if the user has one of them
    if (roles && !roles.includes(user.role)) {
        toast.error("You don't have permission to access this page.");
        return <Navigate to="/" replace />;
    }

    return children;
};

export default PrivateRoute;