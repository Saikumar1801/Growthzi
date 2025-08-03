 
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import useAuth from '../hooks/useAuth';
import toast from 'react-hot-toast';

const Signup = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { signup } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await toast.promise(
                signup(email, password),
                {
                    loading: 'Creating account...',
                    success: 'Account created successfully! Logging you in...',
                    error: (err) => err.response?.data?.error || 'Signup failed. Please try again.',
                }
            );
            navigate('/');
        } catch (error) {
            // Toast handles the error message
        }
    };

    return (
        <div className="form-container">
            <h1>Create Account</h1>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="email">Email Address</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        minLength="8"
                    />
                </div>
                <button type="submit" className="btn btn-primary btn-block">Sign Up</button>
            </form>
            <p className="form-link">
                Already have an account? <Link to="/login">Login</Link>
            </p>
        </div>
    );
};

export default Signup;