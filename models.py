from app import db
from datetime import datetime

# -----------------------------
# Modèle des membres
# -----------------------------
class Membre(db.Model):
    __tablename__ = "membre"
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    postnom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(50), nullable=False)
    
    dimes = db.relationship("Dime", backref="membre", lazy=True)

    def __repr__(self):
        return f"<Membre {self.nom} {self.postnom}>"

# -----------------------------
# Modèle des dîmes
# -----------------------------
class Dime(db.Model):
    __tablename__ = "dime"
    
    id = db.Column(db.Integer, primary_key=True)
    membre_id = db.Column(db.Integer, db.ForeignKey("membre.id"), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    montant = db.Column(db.Float, nullable=False)
    monnaie = db.Column(db.String(10), nullable=False)  # "FC" ou "USD"
    numero_recu = db.Column(db.String(20), nullable=True)  # Numéro de reçu format Mmjj#

    def __repr__(self):
        return f"<Dime {self.membre.nom} {self.montant} {self.monnaie}>"

# -----------------------------
# Optionnel : Modèle utilisateurs pour la connexion
# -----------------------------
class Utilisateur(db.Model):
    __tablename__ = "utilisateur"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # mot de passe hashé

    def __repr__(self):
        return f"<Utilisateur {self.username}>"
