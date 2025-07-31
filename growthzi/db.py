from pymongo import MongoClient
from flask import g

db = None

def init_db(app):
    """Initializes the database connection."""
    global db
    if db is None:
        client = MongoClient(app.config['MONGO_URI'])
        # The 'g' object is a special Flask object that is unique for each request.
        # We store the database connection here to be accessed throughout the request.
        # For simplicity in this project, we'll connect once and reuse the client.
        # The database name is extracted from the URI.
        db_name = app.config['MONGO_URI'].split('/')[-1].split('?')[0]
        db = client[db_name]
    return db

def get_db():
    """Returns the database instance."""
    if db is None:
        raise Exception("Database not initialized. Call init_db() first.")
    return db 
