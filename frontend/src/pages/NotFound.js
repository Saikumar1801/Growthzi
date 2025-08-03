import { Link } from 'react-router-dom';

const NotFound = () => {
    return (
        <div className="not-found-container">
            <h1>404</h1>
            <p>Oops! The page you're looking for doesn't exist.</p>
            <Link to="/" className="btn btn-primary">Go to Dashboard</Link>
        </div>
    );
};

export default NotFound; 
