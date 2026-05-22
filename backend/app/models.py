from datetime import datetime
from . import db

class File(db.Model):
    id = db.Column(db.Integer, primary_key = True, index = True)
    file_name = db.Column(db.String(100), nullable = False)
    file_type = db.Column(db.String(10), nullable = False)
    file_url = db.Column(db.String(200), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)