from pymongo import MongoClient
from flask import current_app, g
import certifi # <-- Import certifi

_mongo_client = None

def get_db_client():
    """
    Returns the single MongoClient instance, creating one if it doesn't exist.
    This version includes SSL certificate handling for deployment environments.
    """
    global _mongo_client
    if _mongo_client is None:
        mongo_uri = current_app.config.get('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI is not set in the application configuration.")
        
        # --- FIX: Explicitly provide the SSL certificate authority file ---
        # This tells PyMongo to use the certificates bundled with the 'certifi' package,
        # resolving SSL handshake errors in many deployment environments like On-Render.
        ca = certifi.where()
        _mongo_client = MongoClient(mongo_uri, tlsCAFile=ca)
        # -----------------------------------------------------------------

    return _mongo_client

def get_db():
    """
    Returns a database instance for the current application context.
    """
    if 'db' not in g:
        client = get_db_client()
        g.db = client.get_database()
    return g.db

def close_db(e=None):
    """
    This function is registered to be called when the application context ends.
    """
    g.pop('db', None)

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)
