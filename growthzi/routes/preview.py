from flask import Blueprint, jsonify, render_template
from bson import ObjectId
from ..db import get_db

preview_bp = Blueprint('preview_bp', __name__)

@preview_bp.route('/<website_id>', methods=['GET'])
def render_website_preview(website_id):
    """
    Fetches website data by ID and renders it using an HTML template.
    This route is public and does not require authentication.
    """
    db = get_db()
    
    try:
        website_data = db.websites.find_one({"_id": ObjectId(website_id)})
    except Exception:
        return "Invalid Website ID format.", 400

    if not website_data:
        return "Website not found.", 404
        
    # The render_template function looks in the 'templates' folder.
    # We pass the fetched data to the template under the variable name 'website'.
    return render_template('index.html', website=website_data)