from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    username = "amaninguba"
    password = "aman4321"
    
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    
    user = User.query.filter_by(username=username).first()
    if user:
        # Met à jour le mot de passe si l'utilisateur existe
        user.password = hashed_password
        print("✅ Mot de passe admin mis à jour !")
    else:
        # Crée un nouvel utilisateur admin
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        print("✅ Utilisateur admin créé !")
    
    db.session.commit()
    print("✅ Base de données mise à jour avec succès !")
