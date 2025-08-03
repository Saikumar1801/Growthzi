import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

import { AuthProvider } from './contexts/AuthContext';
import PrivateRoute from './components/PrivateRoute';
import Layout from './components/Layout';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import WebsiteEditor from './pages/WebsiteEditor';
import AdminPanel from './pages/AdminPanel';
import NotFound from './pages/NotFound';

import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Toaster position="top-center" reverseOrder={false} />
        <Layout>
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />

            {/* Private Routes */}
            <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
            <Route path="/website/:id/edit" element={<PrivateRoute><WebsiteEditor /></PrivateRoute>} />
            <Route 
              path="/admin" 
              element={
                <PrivateRoute roles={['Admin']}>
                  <AdminPanel />
                </PrivateRoute>
              } 
            />
            
            {/* Not Found Route */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Layout>
      </Router>
    </AuthProvider>
  );
}

export default App; 
