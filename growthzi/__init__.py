from flask import Flask
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from .config import Config
from . import db

def seed_database():
    """
    Seeds the database with default roles and a default admin user
    if they don't already exist.
    """
    database = db.get_db()

    # Use upsert to ensure roles exist without creating duplicates
    roles_to_seed = [
        {"name": "Admin", "permissions": ["users:manage", "roles:manage", "websites:create", "websites:read_all", "websites:edit_all", "websites:delete_all", "websites:read_own"]},
        {"name": "Editor", "permissions": ["websites:create", "websites:read_own", "websites:edit_own", "websites:delete_own"]},
        {"name": "Viewer", "permissions": ["websites:read_all", "websites:read_own"]}
    ]
    print("Ensuring default roles exist...")
    for role_data in roles_to_seed:
        db.get_db().roles.update_one({"name": role_data["name"]}, {"$setOnInsert": role_data}, upsert=True)
    print("Default roles are present.")

    # Ensure default admin user exists
    admin_email = "admin@growthzi.com"
    if database.users.find_one({"email": admin_email}) is None:
        print(f"Creating default admin user: {admin_email}")
        admin_role = database.roles.find_one({"name": "Admin"})
        if admin_role:
            hashed_password = generate_password_hash("admin123")
            import datetime
            database.users.insert_one({
                "email": admin_email,
                "password": hashed_password,
                "role_id": admin_role['_id'],
                "created_at": datetime.datetime.now(datetime.timezone.utc)
            })
            print("Default admin user created successfully.")
        else:
            print("CRITICAL ERROR: 'Admin' role not found. Cannot create admin user.")

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register the teardown function to close DB connection after each request
    db.init_app(app)

    # Seed the database within an application context
    with app.app_context():
        seed_database()

    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.websites import websites_bp
    from .routes.preview import preview_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin/')
    app.register_blueprint(websites_bp, url_prefix='/api/websites/')
    app.register_blueprint(preview_bp, url_prefix='/preview')

    return app
