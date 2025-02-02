import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:HelloHackers1994%40%2A@localhost:5432/PharmaDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False