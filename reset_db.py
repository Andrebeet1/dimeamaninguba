# reset_db.py
from app import app, db  # Assure-toi que 'app' est bien importé

if __name__ == "__main__":
    with app.app_context():  # ⚠️ crée le contexte de l'application
        print("Suppression des tables existantes...")
        db.drop_all()
        print("Recréation des tables...")
        db.create_all()
        print("Base de données réinitialisée !")
