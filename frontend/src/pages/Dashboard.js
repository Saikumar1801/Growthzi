 
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import * as websiteApi from '../api/websites';
import useAuth from '../hooks/useAuth';
import WebsiteCard from '../components/WebsiteCard';
import Modal from '../components/Modal';
import Loader from '../components/Loader';

const Dashboard = () => {
    const [websites, setWebsites] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isGenerating, setIsGenerating] = useState(false);
    
    const [businessType, setBusinessType] = useState('');
    const [industry, setIndustry] = useState('');
    
    const [websiteToDelete, setWebsiteToDelete] = useState(null);

    const navigate = useNavigate();
    const { user } = useAuth();
    
    // Permission check for generator
    const canCreate = user?.role === 'Admin' || user?.role === 'Editor';

    const fetchWebsites = async () => {
        try {
            const response = await websiteApi.getWebsites();
            setWebsites(response.data);
        } catch (error) {
            toast.error("Failed to fetch websites.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchWebsites();
    }, []);

    const handleGenerate = async (e) => {
        e.preventDefault();
        setIsGenerating(true);
        try {
            await websiteApi.generateWebsite(businessType, industry);
            toast.success('Website generated successfully!');
            setIsModalOpen(false);
            setBusinessType('');
            setIndustry('');
            fetchWebsites(); // Refresh the list
        } catch (error) {
            toast.error(error.response?.data?.error || "Failed to generate website.");
        } finally {
            setIsGenerating(false);
        }
    };

    const handleEdit = (id) => {
        navigate(`/website/${id}/edit`);
    };

    const confirmDelete = (website) => {
        setWebsiteToDelete(website);
    };
    
    const handleDelete = async () => {
        if (!websiteToDelete) return;
        try {
            await toast.promise(
                websiteApi.deleteWebsite(websiteToDelete._id),
                {
                    loading: 'Deleting website...',
                    success: 'Website deleted successfully!',
                    error: 'Failed to delete website.',
                }
            );
            setWebsites(websites.filter(w => w._id !== websiteToDelete._id));
            setWebsiteToDelete(null); // Close modal
        } catch (error) {
            // toast handles error
        }
    };

    if (isLoading) {
        return <Loader />;
    }

    return (
        <>
            <div className="page-header">
                <h1>My Websites</h1>
                {canCreate && (
                    <button className="btn btn-primary" onClick={() => setIsModalOpen(true)}>
                        + Generate New Website
                    </button>
                )}
            </div>

            {websites.length > 0 ? (
                <div className="grid">
                    {websites.map((website) => (
                        <WebsiteCard
                            key={website._id}
                            website={website}
                            onEdit={handleEdit}
                            onDelete={confirmDelete}
                        />
                    ))}
                </div>
            ) : (
                <p>You haven't created any websites yet. Click 'Generate New Website' to start!</p>
            )}

            <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Generate a New Website with AI">
                <form onSubmit={handleGenerate}>
                    <p>Describe your business and let our AI create a website for you.</p>
                    <div className="form-group">
                        <label htmlFor="businessType">Business Type</label>
                        <input
                            id="businessType"
                            type="text"
                            placeholder="e.g., A small artisanal coffee shop"
                            value={businessType}
                            onChange={(e) => setBusinessType(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="industry">Industry</label>
                        <input
                            id="industry"
                            type="text"
                            placeholder="e.g., Food and Beverage"
                            value={industry}
                            onChange={(e) => setIndustry(e.target.value)}
                            required
                        />
                    </div>
                    <div className="modal-actions">
                        <button type="button" className="btn btn-secondary" onClick={() => setIsModalOpen(false)}>Cancel</button>
                        <button type="submit" className="btn btn-primary" disabled={isGenerating}>
                            {isGenerating ? 'Generating...' : 'Generate'}
                        </button>
                    </div>
                </form>
            </Modal>
            
            <Modal isOpen={!!websiteToDelete} onClose={() => setWebsiteToDelete(null)} title="Confirm Deletion">
                <p>Are you sure you want to delete the website "<strong>{websiteToDelete?.content.title}</strong>"? This action cannot be undone.</p>
                 <div className="modal-actions">
                    <button type="button" className="btn btn-secondary" onClick={() => setWebsiteToDelete(null)}>Cancel</button>
                    <button type="button" className="btn btn-danger" onClick={handleDelete}>Delete</button>
                </div>
            </Modal>
        </>
    );
};

export default Dashboard;