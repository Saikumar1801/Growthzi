from pymongo import MongoClient
from flask import current_app, g
import certifi
import ssl # Import the ssl module

# This will hold the single, persistent client connection for the application.
_mongo_client = None

def get_db_client():
    """
    Returns the single MongoClient instance, creating one if it doesn't exist.
    This version includes explicit, robust SSL/TLS settings for modern cloud databases.
    """
    global _mongo_client
    if _mongo_client is None:
        mongo_uri = current_app.config.get('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI is not set in the application configuration.")
        
        # --- THE DEFINITIVE SSL/TLS FIX ---
        
        # 1. Get the path to the trusted certificate authorities from certifi.
        ca = certifi.where()
        
        # 2. Create the MongoClient with explicit, secure TLS options.
        #    - tls=True: Enforces that the connection must use TLS.
        #    - tlsCAFile=ca: Specifies the trusted certificates to use for verification.
        #    - tlsVersion=ssl.PROTOCOL_TLSv1_2: Forces the use of the modern and widely
        #      supported TLSv1.2 protocol, which can resolve handshake failures.
        _mongo_client = MongoClient(
            mongo_uri, 
            tls=True, 
            tlsCAFile=ca,
            tlsVersion=ssl.PROTOCOL_TLSv1_2 
        )
        # ------------------------------------

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
