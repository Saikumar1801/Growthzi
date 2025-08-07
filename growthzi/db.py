from pymongo import MongoClient
from flask import current_app, g
import certifi

def get_db():
    """
    Connects to the database for the current request.
    If a connection is already established for this request, returns it.
    """
    if 'db_client' not in g:
        # Get the path to the trusted certificate authorities from certifi.
        ca = certifi.where()
        
        # Connect using the URI and the certifi CA file.
        # This is the most common and robust configuration for cloud deployments.
        g.db_client = MongoClient(
            current_app.config['MONGO_URI'],
            tls=True,
            tlsCAFile=ca
        )
        
        g.db = g.db_client.get_database()
    return g.db

def close_db(e=None):
    """Closes the database connection at the end of the request."""
    client = g.pop('db_client', None)
    if client is not None:
        client.close()

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)