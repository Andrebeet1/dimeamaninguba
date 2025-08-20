from app import app
from models import db

# Crée les tables définies dans models.py
with app.app_context():
    db.create_all()
    print("Tables créées avec succès !")
