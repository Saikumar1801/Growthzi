from pymongo import MongoClient
from flask import current_app, g
import certifi
import ssl

def get_db():
    """
    Connects to the database for the current request.
    If a connection is already established for this request, returns it.
    """
    if 'db_client' not in g:
        # This code will only run once per request.
        ca = certifi.where()
        
        # --- THE FIX: Correct the parameter name to tls_version ---
        g.db_client = MongoClient(
            current_app.config['MONGO_URI'],
            tls=True,
            tlsCAFile=ca,
            tls_version=ssl.PROTOCOL_TLSv1_2 # <-- Corrected from tlsVersion
        )
        # --------------------------------------------------------
        
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
