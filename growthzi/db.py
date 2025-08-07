from pymongo import MongoClient
from flask import current_app, g
import certifi
import ssl

def get_db():
    if 'db_client' not in g:
        ca = certifi.where()
        g.db_client = MongoClient(
            current_app.config['MONGO_URI'],
            tls=True,
            tlsCAFile=ca,
            tlsVersion=ssl.TLSVersion.TLSv1_2  # Corrected parameter
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

