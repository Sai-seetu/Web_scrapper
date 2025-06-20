from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
from flask_migrate import Migrate

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
scheduler = BackgroundScheduler()

app = Flask(__name__, template_folder="../templates")
app.secret_key = 'dev_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/scraper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    migrate.init_app(app, db)
    from app.routes import *
    scheduler.start()