from pymongo import MongoClient
from pymongo.database import Database
from flask import current_app, g

# This is a placeholder for the global database connection object.
# It's better to manage it within the Flask application context.
_db_client = None
_db = None

def get_db_client():
    """
    Returns the MongoClient instance, creating one if it doesn't exist.
    This function can be used to access the client itself if needed.
    """
    global _db_client
    if _db_client is None:
        mongo_uri = current_app.config.get('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI is not set in the application configuration.")
        _db_client = MongoClient(mongo_uri)
    return _db_client

def get_db():
    """
    Returns a database instance for the current application context.
    It intelligently gets the database name from the connection URI.
    """
    # Use Flask's 'g' object to store the db connection for the life of a request.
    # This prevents creating a new connection for every db call within the same request.
    if 'db' not in g:
        client = get_db_client()
        # PyMongo's get_database() method is the standard way to get a DB instance.
        # If a database is specified in the MONGO_URI, it will be used.
        # If not, it will raise a ConfigurationError, which is more descriptive.
        # This avoids the fragile string splitting.
        g.db = client.get_database()

    return g.db

def init_db(app):
    """
    Initializes the database connection and registers a teardown function
    to close the client when the application context ends.
    """
    # The 'with app.app_context()' in create_app ensures this runs with an active app context.
    get_db_client() # Establish the initial client connection.

    @app.teardown_appcontext
    def teardown_db(exception=None):
        # This function will be called when the app context is popped.
        # While modern PyMongo handles connection pooling well, it's good practice
        # to have a cleanup mechanism, though closing the client is often not necessary
        # for long-running applications. We'll pop the 'db' from 'g'.
        db = g.pop('db', None)
        # Note: We are not closing the client here (_db_client.close()) because
        # in many web server configurations (like gunicorn with workers),
        # you want the client to persist across requests for performance.
        # The connection pool will manage individual connections.

# This init_db_command function is optional but useful for CLI commands like `flask init-db`
# You can remove it if you don't plan to add custom CLI commands.
def init_db_command():
    """Clear the existing data and create new tables."""
    # This is a placeholder for any manual database setup you might need.
    # For this project, the seeding in create_app() is sufficient.
    print("Database command placeholder.")

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(teardown_db)
    # If you want a `flask init-db` command, you would register it here.
    # from flask.cli import with_appcontext
    # app.cli.add_command(click.Command('init-db', callback=with_appcontext(init_db_command)))
