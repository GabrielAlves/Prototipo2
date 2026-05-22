from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app(test_config = None):
    app = Flask(__name__)
    
    cors_origins = os.getenv("CORS_ORIGINS", "")

    if cors_origins.strip():
        origins = [
            origin.strip()
            for origin in cors_origins.split(",")
            if origin.strip()
        ]
    else:
        origins = ["*"]

    CORS(
        app,
        origins=origins,
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-API-Key"]
    )

    if test_config:
        app.config.update(test_config)

    else:
        from .config import Config
        app.config.from_object(Config)

    from . import routes
    app.register_blueprint(routes.bp)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app