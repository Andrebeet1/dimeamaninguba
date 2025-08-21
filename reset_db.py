# reset_db.py
from app import db

# Supprimer toutes les tables existantes
db.drop_all()
db.create_all()  # Facultatif si tu veux recréer directement
print("Tables réinitialisées !")
