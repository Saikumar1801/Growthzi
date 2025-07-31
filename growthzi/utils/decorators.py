from functools import wraps
import jwt
from flask import request, jsonify, current_app, g
from bson import ObjectId
from ..db import get_db

def permission_required(*permissions):
    """
    A decorator to protect routes with role-based permissions.
    - permissions: A list of permission strings (e.g., 'roles:manage', 'websites:edit_own').
      The user must have at least ONE of these permissions to proceed.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            db = get_db()
            auth_header = request.headers.get('Authorization')
            token = None

            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Authorization header is missing or invalid"}), 401

            try:
                token = auth_header.split(" ")[1]
                payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                user_id = payload['user_id']
                
                user = db.users.find_one({"_id": ObjectId(user_id)})
                if not user:
                    return jsonify({"error": "User not found"}), 401

                role = db.roles.find_one({"_id": user.get('role_id')})
                if not role:
                     return jsonify({"error": "User role not found. Data integrity issue."}), 500

                # --- MODIFIED PERMISSION CHECK ---
                user_permissions = role.get('permissions', [])
                
                # Check if the user has ANY of the required permissions
                if not any(p in user_permissions for p in permissions):
                    return jsonify({"error": "Forbidden: You don't have the required permission for this action"}), 403

                # Make user info available to the route via Flask's 'g' object
                g.current_user = user
                g.current_user_role = role

            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except (jwt.InvalidTokenError, KeyError):
                return jsonify({"error": "Invalid token"}), 401
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator