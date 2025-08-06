from flask import Blueprint, request, jsonify
from bson import ObjectId
from ..db import get_db
from ..utils.decorators import permission_required

admin_bp = Blueprint('admin_bp', __name__)

# --- Role Management ---
# (get_roles and create_role functions remain the same)

@admin_bp.route('/roles', methods=['GET'])
@permission_required('roles:manage')
def get_roles():
    """Returns a list of all roles."""
    db = get_db()
    roles_cursor = db.roles.find({})
    roles_list = []
    for role in roles_cursor:
        role['_id'] = str(role['_id'])
        roles_list.append(role)
    return jsonify(roles_list), 200

# ... (create_role function is unchanged)

# --- User Management ---

# --- NEW ENDPOINT: Get all users with their roles ---
@admin_bp.route('/users', methods=['GET'])
@permission_required('users:manage')
def get_users():
    """
    Returns a list of all users, including their role name.
    This is an admin-only endpoint.
    """
    db = get_db()
    # Use an aggregation pipeline to join users with roles collection
    users_pipeline = [
        {
            "$lookup": {
                "from": "roles", # The collection to join with
                "localField": "role_id", # Field from the users collection
                "foreignField": "_id", # Field from the roles collection
                "as": "role_info" # The new array field to add
            }
        },
        {
            "$unwind": { # Deconstruct the role_info array to a single object
                "path": "$role_info",
                "preserveNullAndEmptyArrays": True # Keep users even if they have no role
            }
        },
        {
            "$project": { # Select the fields to return
                "_id": 1,
                "email": 1,
                "created_at": 1,
                "role": "$role_info.name" # Rename role_info.name to role
            }
        }
    ]
    
    users_cursor = db.users.aggregate(users_pipeline)
    users_list = []
    for user in users_cursor:
        user['_id'] = str(user['_id'])
        # Ensure a user with a missing role doesn't break the frontend
        if 'role' not in user:
            user['role'] = 'N/A' 
        users_list.append(user)
        
    return jsonify(users_list), 200
# ----------------------------------------------------

@admin_bp.route('/users/<user_id>/assign-role', methods=['PUT'])
@permission_required('users:manage')
def assign_role(user_id):
    """Assigns a role to a user."""
    db = get_db()
    data = request.get_json()
    role_name = data.get('role_name')

    if not role_name:
        return jsonify({"error": "role_name is required"}), 400

    role = db.roles.find_one({"name": role_name})
    if not role:
        return jsonify({"error": f"Role '{role_name}' not found"}), 404
        
    try:
        user_to_update = db.users.find_one({"_id": ObjectId(user_id)})
        if not user_to_update:
            return jsonify({"error": "User not found"}), 404
    except Exception:
        return jsonify({"error": "Invalid user_id format"}), 400

    result = db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role_id": role['_id']}}
    )

    if result.modified_count == 0:
        return jsonify({"message": "User already has this role or user not found"}), 200

    return jsonify({"message": f"User {user_id} assigned role '{role_name}'"}), 200