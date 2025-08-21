# create_admin.py
from app import db
from models import User
from werkzeug.security import generate_password_hash

def create_admin_user():
    username = "amaninguba"
    password = "tonpassword"
    
    user = User.query.filter_by(username=username).first()
    if not user:
        admin = User(username=username, password=generate_password_hash(password))
        db.session.add(admin)
        db.session.commit()
        print(f"Admin {username} créé")
    else:
        print(f"Admin {username} déjà existant")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        create_admin_user()
