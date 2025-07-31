from flask import Blueprint, request, jsonify
from bson import ObjectId
from ..db import get_db
from ..utils.decorators import permission_required

admin_bp = Blueprint('admin_bp', __name__)

# --- Role Management ---

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

@admin_bp.route('/roles', methods=['POST'])
@permission_required('roles:manage')
def create_role():
    """Creates a new role."""
    db = get_db()
    data = request.get_json()

    if not data or not data.get('name') or not data.get('permissions'):
        return jsonify({"error": "Role name and permissions are required"}), 400

    if db.roles.find_one({"name": data['name']}):
        return jsonify({"error": "Role with this name already exists"}), 409

    role_id = db.roles.insert_one({
        "name": data['name'],
        "permissions": data['permissions']
    }).inserted_id

    return jsonify({"message": "Role created successfully", "role_id": str(role_id)}), 201

# --- User Management ---

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
        # Check if user exists before updating
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