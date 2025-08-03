import useAuth from '../hooks/useAuth';

const WebsiteCard = ({ website, onEdit, onDelete }) => {
    const { user } = useAuth();
    
    const canModify = user?.role === 'Admin' || user?.id === website.owner_id;

    const handlePreview = () => {
        // --- START OF FIX ---

        // The backend runs on port 5000. We need to build the full URL to it.
        // In development, the backend is on http://localhost:5000.
        // In production, you would use your actual domain name.
        const backendUrl = process.env.NODE_ENV === 'production' 
            ? 'https://your-production-domain.com' // Replace with your live domain
            : 'http://localhost:5000';

        const previewUrl = `${backendUrl}/preview/${website._id}`;

        // Open the full URL in a new tab.
        window.open(previewUrl, '_blank');
        
        // --- END OF FIX ---
    };

    return (
        <div className="website-card">
            <h3>{website.content.title}</h3>
            <p>{website.content.hero.headline}</p>
            <div className="card-actions">
                <button onClick={handlePreview} className="btn btn-secondary">
                    Preview
                </button>
                {canModify && (
                    <>
                        <button onClick={() => onEdit(website._id)} className="btn btn-primary">
                            Edit
                        </button>
                        <button onClick={() => onDelete(website)} className="btn btn-danger">
                            Delete
                        </button>
                    </>
                )}
            </div>
        </div>
    );
};

export default WebsiteCard;