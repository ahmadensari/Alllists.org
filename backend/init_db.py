from main import app
from database import db
from models.user import User
from models.list import List
from models.transaction import Transaction

with app.app_context():
    db.create_all()
    print("Database tables created.")
