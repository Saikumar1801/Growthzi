import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from ..db import get_db  # Correctly import the get_db function
from ..utils.decorators import permission_required

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    database = get_db()  # Get the database instance for this request
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    email = data.get('email')
    password = data.get('password')

    if database.users.find_one({"email": email}):
        return jsonify({"error": "User with this email already exists"}), 409

    default_role = database.roles.find_one({"name": "Viewer"})
    if not default_role:
        return jsonify({"error": "Default 'Viewer' role not found in the system."}), 500

    hashed_password = generate_password_hash(password)

    user_id = database.users.insert_one({
        "email": email,
        "password": hashed_password,
        "role_id": default_role['_id'],
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }).inserted_id

    return jsonify({"message": "User created successfully", "user_id": str(user_id)}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    database = get_db()  # Get the database instance for this request
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    email = data.get('email')
    password = data.get('password')

    user = database.users.find_one({"email": email})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({"message": "Login successful", "token": token})


@auth_bp.route('/me', methods=['GET'])
@permission_required('websites:read_own')
def get_current_user():
    """
    Returns essential info for the currently logged-in user, including their role.
    """
    if not g.get('current_user') or not g.get('current_user_role'):
        return jsonify({"error": "User context not found"}), 404
    
    user_info = {
        "id": str(g.current_user['_id']),
        "email": g.current_user['email'],
        "role": g.current_user_role['name']
    }
    return jsonify(user_info), 200
