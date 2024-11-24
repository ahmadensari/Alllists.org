from main import app
from database import db
from models import User, List, Transaction  # Ensure all models are imported here

with app.app_context():
    db.create_all()
    print("Database tables created.")
