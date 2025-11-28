import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    MONGODB_DB_NAME = os.getenv("MONGODB_NAME", "stock_management_db")
    RESTOCK_THRESHOLD = float(os.getenv("RESTOCK_THRESHOLD", 0.2))
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    FLASK_DEBUG = bool(int(os.getenv("FLASK_DEBUG", "0")))
