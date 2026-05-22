import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    # SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://usuario:senha@host:3306/banco"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

    API_KEY = os.getenv("API_KEY")

    STORAGE_MODE = os.getenv("STORAGE_MODE", "local")

    # AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    # AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    # AWS_BUCKET = os.getenv("AWS_BUCKET")
    # AWS_REGION = os.getenv("AWS_REGION")