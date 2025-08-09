from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        db.create_all()

class DateRequest(db.Model):
    __tablename__ = 'date_requests'
    id = db.Column(db.Integer, primary_key=True)
    range_key = db.Column(db.String(100), nullable=False)
    generated_dates = db.Column(db.Text, nullable=False)  # JSON list
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "range_key": self.range_key,
            "generated_dates": json.loads(self.generated_dates),
            "created_at": self.created_at.isoformat()
        }

class RephraseRequest(db.Model):
    __tablename__ = 'rephrase_requests'
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    outputs = db.Column(db.Text, nullable=False)  # JSON list of variants
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "original_text": self.original_text,
            "outputs": json.loads(self.outputs),
            "created_at": self.created_at.isoformat()
        }
