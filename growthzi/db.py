from pymongo import MongoClient
from flask import current_app, g

# This will hold the single, persistent client connection for the application.
_mongo_client = None

def get_db_client():
    """
    Returns the single MongoClient instance, creating one if it doesn't exist.
    This is efficient as it reuses the same connection pool.
    """
    global _mongo_client
    if _mongo_client is None:
        mongo_uri = current_app.config.get('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI is not set in the application configuration.")
        _mongo_client = MongoClient(mongo_uri)
    return _mongo_client

def get_db():
    """
    Returns a database instance for the current application context.
    This is the function that all your routes will call.
    It intelligently gets the database from the client connection.
    """
    # Use Flask's 'g' object to store the db connection for the life of a single request.
    if 'db' not in g:
        client = get_db_client()
        # The get_database() method is the standard way to get a DB instance.
        # If a database is specified in the MONGO_URI, it will be used.
        # If not, it will raise a ConfigurationError, which is more descriptive
        # and prevents the "empty string" error.
        g.db = client.get_database()

    return g.db

def close_db(e=None):
    """
    This function is registered to be called when the application context ends.
    It removes the database connection from the 'g' object.
    We don't close the client itself, to allow for connection reuse.
    """
    g.pop('db', None)

def init_app(app):
    """Register database functions with the Flask app. This is called from create_app."""
    app.teardown_appcontext(close_db)
