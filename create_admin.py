from app import app, db, User
from werkzeug.security import generate_password_hash
import os

def create_admin_user():
    with app.app_context():
        # Récupérer nom d'utilisateur et mot de passe depuis les variables d'environnement
        username = os.environ.get('ADMIN_USERNAME', 'amaninguba')
        password = os.environ.get('ADMIN_PASSWORD', 'amani4321')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"L'utilisateur '{username}' existe déjà !")
            return

        admin_user = User(
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Utilisateur admin '{username}' créé avec succès !")

if __name__ == "__main__":
    create_admin_user()
