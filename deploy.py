# deploy.py
import os
from app import app, db
from create_admin import create_admin_user  # à adapter selon ton create_admin.py

# 1️⃣ Créer les tables si elles n'existent pas
with app.app_context():
    print("Création des tables...")
    db.create_all()
    print("Tables créées ✅")

# 2️⃣ Créer l'utilisateur admin
print("Création de l'utilisateur admin...")
create_admin_user()  # Assure-toi que cette fonction existe dans create_admin.py
print("Admin créé ✅")

# 3️⃣ Lancer Gunicorn
print("Démarrage de Gunicorn...")
os.system("gunicorn app:app --bind 0.0.0.0:$PORT")
