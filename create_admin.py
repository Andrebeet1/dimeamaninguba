# create_admin.py
from werkzeug.security import generate_password_hash
from app import app, db
from models import User

def create_admin_user():
    username = "amaninguba"   # 🔑 identifiant admin
    password = "tonpassword"  # 🔑 change ce mot de passe !

    with app.app_context():
        # Vérifie si l'admin existe déjà
        user = User.query.filter_by(username=username).first()
        if not user:
            admin = User(
                username=username,
                password=generate_password_hash(password)  # hash pour sécurité
            )
            db.session.add(admin)
            db.session.commit()
            print(f"✅ Admin '{username}' créé avec succès")
        else:
            print(f"⚠️ Admin '{username}' existe déjà")

if __name__ == "__main__":
    create_admin_user()
