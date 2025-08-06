import datetime
import os
import json
from flask import Blueprint, request, jsonify, g
from bson import ObjectId
import google.generativeai as genai # Import Google's library
from ..db import get_db
from ..utils.decorators import permission_required

websites_bp = Blueprint('websites_bp', __name__)

# --- Configure Google Gemini API ---
# The API key is loaded from config, which reads from .env
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Helper to serialize BSON ObjectId to string
def serialize_website(doc):
    if doc.get('_id'): doc['_id'] = str(doc['_id'])
    if doc.get('owner_id'): doc['owner_id'] = str(doc['owner_id'])
    return doc

# --- AI Content Generation (with Gemini) ---

@websites_bp.route('/generate', methods=['POST'])
@permission_required('websites:create')
def generate_website():
    db = get_db()
    data = request.get_json()
    
    if not data or not data.get('business_type') or not data.get('industry'):
        return jsonify({"error": "business_type and industry are required"}), 400

    business_type = data.get('business_type')
    industry = data.get('industry')
    
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        Generate website content for a company.
        - Business Type: {business_type}
        - Industry: {industry}
        
        The output MUST be a single, valid JSON object. Do not include any text, notes, or markdown formatting like ```json before or after the JSON object.
        The JSON structure should be exactly this:
        {{
          "title": "A short, catchy company name",
          "hero": {{
            "headline": "A powerful headline (max 10 words)",
            "subheading": "An engaging subheading that explains more (max 20 words)",
            "cta_button_text": "A call-to-action button text (max 4 words)"
          }},
          "about": {{
            "title": "About Us",
            "text": "A descriptive paragraph about the company's mission and values (around 50 words)."
          }},
          "services": [
            {{ "name": "Service One Name", "description": "A brief description of the first service (around 20 words)." }},
            {{ "name": "Service Two Name", "description": "A brief description of the second service (around 20 words)." }},
            {{ "name": "Service Three Name", "description": "A brief description of the third service (around 20 words)." }}
          ]
        }}
        """
        
        response = model.generate_content(prompt)
        # Parse the text response into a JSON object
        generated_content = json.loads(response.text)

    except json.JSONDecodeError:
        print(f"Gemini API did not return valid JSON. Response:\n{response.text}")
        return jsonify({"error": "Failed to parse content from AI service. The response was not valid JSON."}), 500
    except Exception as e:
        print(f"Google Gemini API Error: {e}")
        return jsonify({"error": "Failed to generate content from AI service."}), 500

    # Store in Database
    website_doc = {
        "owner_id": g.current_user['_id'],
        "created_at": datetime.datetime.now(datetime.timezone.utc),
        "updated_at": datetime.datetime.now(datetime.timezone.utc),
        "content": generated_content
    }
    
    result = db.websites.insert_one(website_doc)
    
    return jsonify({
        "message": "Website generated and created successfully", 
        "website": serialize_website(website_doc)
    }), 201

# --- Standard CRUD Operations ---

@websites_bp.route('/', methods=['GET'])
@permission_required('websites:read_all', 'websites:read_own')
def get_websites():
    db = get_db()
    user_role = g.current_user_role['name']
    user_id = g.current_user['_id']
    
    query = {}
    if user_role == 'Editor':
        query = {"owner_id": user_id}

    websites_cursor = db.websites.find(query)
    websites_list = [serialize_website(doc) for doc in websites_cursor]
    
    return jsonify(websites_list), 200

@websites_bp.route('/<website_id>', methods=['GET'])
@permission_required('websites:read_all', 'websites:read_own')
def get_website_by_id(website_id):
    db = get_db()
    try:
        website = db.websites.find_one({"_id": ObjectId(website_id)})
        if not website:
            return jsonify({"error": "Website not found"}), 404
        return jsonify(serialize_website(website)), 200
    except Exception:
        return jsonify({"error": "Invalid website_id format"}), 400

@websites_bp.route('/<website_id>', methods=['PUT'])
@permission_required('websites:edit_all', 'websites:edit_own')
def update_website(website_id):
    db = get_db()
    data = request.get_json()
    if 'content' not in data:
        return jsonify({"error": "Request body must contain 'content' field"}), 400

    try:
        website_to_update = db.websites.find_one({"_id": ObjectId(website_id)})
        if not website_to_update:
            return jsonify({"error": "Website not found"}), 404
        
        user_role = g.current_user_role['name']
        is_owner = str(website_to_update['owner_id']) == str(g.current_user['_id'])
        
        if user_role == 'Editor' and not is_owner:
            return jsonify({"error": "Forbidden: You can only edit your own websites"}), 403

        db.websites.update_one(
            {"_id": ObjectId(website_id)},
            {"$set": {"content": data['content'], "updated_at": datetime.datetime.now(datetime.timezone.utc)}}
        )
        updated_website = db.websites.find_one({"_id": ObjectId(website_id)})
        return jsonify(serialize_website(updated_website)), 200
    except Exception:
        return jsonify({"error": "Invalid website_id format"}), 400

@websites_bp.route('/<website_id>', methods=['DELETE'])
@permission_required('websites:delete_all', 'websites:delete_own')
def delete_website(website_id):
    db = get_db()
    try:
        website_to_delete = db.websites.find_one({"_id": ObjectId(website_id)})
        if not website_to_delete:
            return jsonify({"error": "Website not found"}), 404

        user_role = g.current_user_role['name']
        is_owner = str(website_to_delete['owner_id']) == str(g.current_user['_id'])
        
        if user_role == 'Editor' and not is_owner:
            return jsonify({"error": "Forbidden: You can only delete your own websites"}), 403

        db.websites.delete_one({"_id": ObjectId(website_id)})
        return jsonify({"message": "Website deleted successfully"}), 200
    except Exception:
        return jsonify({"error": "Invalid website_id format"}), 400