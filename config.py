import os
from dotenv import load_dotenv

load_dotenv()  # Charge le fichier .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "changeme123")  # Clé secrète Flask
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dime.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
