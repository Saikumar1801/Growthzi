from flask import Flask
from flask_cors import CORS
from .config import Config
from . import db  # Import the db module

def seed_database():
    """Seeds the database with default roles if they don't exist."""
    # Use the get_db() function to ensure we have a valid database handle
    database = db.get_db()
    if database.roles.count_documents({}) == 0:
        print("Seeding database with default roles...")
        roles = [
            {
                "name": "Admin",
                "permissions": [
                    "users:manage", "roles:manage",
                    "websites:create", "websites:read_all", "websites:edit_all", "websites:delete_all"
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
        database.roles.insert_many(roles)
        print("Default roles seeded.")

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(Config)

    # Initialize CORS for cross-origin requests from the frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize and register database functions with the app
    db.init_app(app)

    # The app context is needed for database operations like seeding
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
