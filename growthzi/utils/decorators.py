from functools import wraps
import jwt
from flask import request, jsonify, current_app, g
from bson import ObjectId
from ..db import get_db

def permission_required(*permissions):
    """
    A decorator to protect routes with role-based permissions.
    - permissions: A list of permission strings. The user must have at least ONE.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("\n--- PERMISSION CHECK INITIATED ---") # DEBUG
            db = get_db()
            auth_header = request.headers.get('Authorization')
            
            if not auth_header or not auth_header.startswith('Bearer '):
                print("DEBUG: No or invalid Authorization header.")
                return jsonify({"error": "Authorization header is missing or invalid"}), 401

            try:
                token = auth_header.split(" ")[1]
                payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                user_id = payload['user_id']
                print(f"DEBUG: Token decoded. User ID: {user_id}")

                user = db.users.find_one({"_id": ObjectId(user_id)})
                if not user:
                    print(f"DEBUG: User with ID {user_id} NOT FOUND in database.")
                    return jsonify({"error": "User not found"}), 401

                print(f"DEBUG: User found: {user['email']}")

                role = db.roles.find_one({"_id": user.get('role_id')})
                if not role:
                    print(f"DEBUG: Role NOT FOUND for user {user['email']}. Role ID was: {user.get('role_id')}")
                    return jsonify({"error": "User role not found. Data integrity issue."}), 500
                
                print(f"DEBUG: User role found: {role['name']}")

                user_permissions = role.get('permissions', [])
                print(f"DEBUG: User permissions: {user_permissions}")
                print(f"DEBUG: Required permissions (any of): {permissions}")
                
                # Check if the user has ANY of the required permissions
                if not any(p in user_permissions for p in permissions):
                    print("DEBUG: PERMISSION DENIED. User does not have any of the required permissions.")
                    return jsonify({"error": "Forbidden: You don't have the required permission for this action"}), 403

                print("DEBUG: PERMISSION GRANTED.")
                g.current_user = user
                g.current_user_role = role

            except jwt.ExpiredSignatureError:
                print("DEBUG: Token has expired.")
                return jsonify({"error": "Token has expired"}), 401
            except (jwt.InvalidTokenError, KeyError, Exception) as e:
                print(f"DEBUG: Invalid token or other error: {e}")
                return jsonify({"error": "Invalid token"}), 401
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator