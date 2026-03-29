"""MongoDB connection helpers for MicroLibrary."""
from pymongo import MongoClient
from pymongo.database import Database
import os
from functools import lru_cache


@lru_cache
def get_database() -> Database:
    """Create and cache MongoDB database connection."""
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB", "microlibrary")
    client = MongoClient(mongo_uri)
    return client[db_name]
