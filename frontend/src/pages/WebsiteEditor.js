 
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import * as websiteApi from '../api/websites';
import Loader from '../components/Loader';

const WebsiteEditor = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [website, setWebsite] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchWebsite = async () => {
            try {
                const response = await websiteApi.getWebsiteById(id);
                setWebsite(response.data.content);
            } catch (error) {
                toast.error("Could not load website data.");
                navigate('/');
            } finally {
                setIsLoading(false);
            }
        };
        fetchWebsite();
    }, [id, navigate]);

    const handleChange = (e, section, field) => {
        const { value } = e.target;
        setWebsite(prev => ({
            ...prev,
            [section]: {
                ...prev[section],
                [field]: value,
            },
        }));
    };

    const handleServiceChange = (e, index, field) => {
        const { value } = e.target;
        const newServices = [...website.services];
        newServices[index][field] = value;
        setWebsite(prev => ({ ...prev, services: newServices }));
    };

    const addService = () => {
        setWebsite(prev => ({
            ...prev,
            services: [...prev.services, { name: 'New Service', description: 'Description' }]
        }));
    };

    const removeService = (index) => {
        const newServices = website.services.filter((_, i) => i !== index);
        setWebsite(prev => ({ ...prev, services: newServices }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await toast.promise(
                websiteApi.updateWebsite(id, website),
                {
                    loading: 'Saving changes...',
                    success: 'Website updated successfully!',
                    error: 'Failed to save changes.'
                }
            );
            navigate('/');
        } catch (error) {
            // toast handles error
        }
    };

    if (isLoading) {
        return <Loader />;
    }

    if (!website) {
        return <p>Website not found.</p>;
    }

    return (
        <form onSubmit={handleSubmit} className="form-container" style={{maxWidth: '800px'}}>
            <h1>Editing: {website.title}</h1>

            <div className="form-group">
                <label htmlFor="title">Website Title</label>
                <input id="title" value={website.title} onChange={(e) => setWebsite({...website, title: e.target.value})} />
            </div>

            <div className="editor-section">
                <h3>Hero Section</h3>
                <div className="form-group">
                    <label htmlFor="headline">Headline</label>
                    <input id="headline" value={website.hero.headline} onChange={(e) => handleChange(e, 'hero', 'headline')} />
                </div>
                <div className="form-group">
                    <label htmlFor="subheading">Subheading</label>
                    <input id="subheading" value={website.hero.subheading} onChange={(e) => handleChange(e, 'hero', 'subheading')} />
                </div>
            </div>

            <div className="editor-section">
                <h3>Services</h3>
                {website.services.map((service, index) => (
                    <div key={index} className="service-item">
                         <div className="form-group">
                            <label>Service {index + 1} Name</label>
                            <input value={service.name} onChange={(e) => handleServiceChange(e, index, 'name')} />
                         </div>
                         <div className="form-group">
                            <label>Service {index + 1} Description</label>
                            <textarea value={service.description} onChange={(e) => handleServiceChange(e, index, 'description')} />
                         </div>
                         <button type="button" className="btn btn-danger" onClick={() => removeService(index)}>Remove Service</button>
                    </div>
                ))}
                 <button type="button" className="btn btn-secondary" onClick={addService}>+ Add Service</button>
            </div>
            
            <div style={{display: 'flex', gap: '1rem', marginTop: '2rem'}}>
                <button type="button" className="btn btn-secondary" onClick={() => navigate('/')}>Cancel</button>
                <button type="submit" className="btn btn-primary">Save Changes</button>
            </div>
        </form>
    );
};

export default WebsiteEditor;