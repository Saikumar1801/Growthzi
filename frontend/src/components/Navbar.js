import { Link, NavLink } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

const Navbar = () => {
    const { isAuthenticated, user, logout } = useAuth();

    return (
        <nav className="navbar">
            <Link to={isAuthenticated ? "/" : "/login"} className="navbar-brand">
                Growthzi
            </Link>
            <div className="navbar-links">
                {isAuthenticated ? (
                    <>
                        <NavLink to="/">Dashboard</NavLink>
                        {user?.role === 'Admin' && <NavLink to="/admin">Admin Panel</NavLink>}
                        <button onClick={logout} className="logout-button">Logout</button>
                    </>
                ) : (
                    <>
                        <NavLink to="/login">Login</NavLink>
                        <NavLink to="/signup">Sign Up</NavLink>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navbar; 
