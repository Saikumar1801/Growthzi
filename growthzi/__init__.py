from flask import Flask
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from .config import Config
from .db import init_db, get_db

def seed_database():
    """
    Seeds the database with default roles and a default admin user
    if they don't already exist. This is now more robust.
    """
    db = get_db()

    # --- 1. Define Roles and ensure they exist ---
    print("Ensuring default roles exist...")
    roles_to_seed = [
        {
            "name": "Admin",
            "permissions": [
                "users:manage", "roles:manage",
                "websites:create", "websites:read_all", "websites:edit_own", "websites:delete_all",
                "websites:read_own"  # <-- ADD THIS MISSING PERMISSION
            ]
        },
        {
            "name": "Editor",
            "permissions": [
                "websites:create", "websites:read_own", "websites:edit_own", "websites:delete_own"
            ]
        },
        {
            "name": "Viewer",
            "permissions": ["websites:read_all", "websites:read_own"]
        }
    ]

    for role_data in roles_to_seed:
        # Using update_one with upsert=True is an idempotent way to seed.
        # It finds a role by name, and if it doesn't exist, it inserts it.
        db.roles.update_one(
            {"name": role_data["name"]},
            {"$setOnInsert": role_data},
            upsert=True
        )
    print("Default roles are present.")


    # --- 2. Seed Default Admin User ---
    admin_email = "admin@growthzi.com"
    
    # Check if the admin user already exists
    if db.users.find_one({"email": admin_email}) is None:
        print(f"Creating default admin user: {admin_email}")
        
        # This is now guaranteed to find the 'Admin' role
        admin_role = db.roles.find_one({"name": "Admin"})
        
        # This check is still good practice
        if not admin_role:
            print("CRITICAL ERROR: 'Admin' role could not be found or created. Cannot create default admin.")
            return

        admin_password = "admin123"
        hashed_password = generate_password_hash(admin_password)

        import datetime
        db.users.insert_one({
            "email": admin_email,
            "password": hashed_password,
            "role_id": admin_role['_id'],
            "created_at": datetime.datetime.now(datetime.timezone.utc)
        })
        print("Default admin user created successfully.")

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    with app.app_context():
        init_db(app)
        seed_database()

    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.websites import websites_bp
    from .routes.preview import preview_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin/')
    app.register_blueprint(websites_bp, url_prefix='/api/websites/')
    app.register_blueprint(preview_bp, url_prefix='/preview')

    return app