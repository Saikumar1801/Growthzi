import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from ..db import get_db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    db = get_db()
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    email = data.get('email')
    password = data.get('password')

    if db.users.find_one({"email": email}):
        return jsonify({"error": "User with this email already exists"}), 409

    # Find the default 'Editor' role
    editor_role = db.roles.find_one({"name": "Editor"})
    if not editor_role:
        return jsonify({"error": "Default user role not configured in the system."}), 500

    hashed_password = generate_password_hash(password)

    user_id = db.users.insert_one({
        "email": email,
        "password": hashed_password,
        "role_id": editor_role['_id'], # <-- Use role_id instead of string
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }).inserted_id

    return jsonify({"message": "User created successfully", "user_id": str(user_id)}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    db = get_db()
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    email = data.get('email')
    password = data.get('password')

    user = db.users.find_one({"email": email})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT token. The payload now only needs the user_id.
    # The decorator will handle fetching permissions on each request.
    token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({"message": "Login successful", "token": token})