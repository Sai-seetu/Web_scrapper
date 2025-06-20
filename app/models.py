from app import db
from datetime import datetime

class APILink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String(255))
    website_url = db.Column(db.String(1000))
    video_path = db.Column(db.String(255))
    scraped_text = db.Column(db.Text)  # <-- Add this
    interval = db.Column(db.String(10))
    active = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    api_endpoint = db.Column(db.String(500))