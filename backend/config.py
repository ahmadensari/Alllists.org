import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://ahmadensari:Mahmood#7407Ifi@localhost/alllists_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
