from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"  # ✅ éviter le mot réservé "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Membre(db.Model):
    __tablename__ = "membres"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    postnom = db.Column(db.String(50), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    adresse = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(20), nullable=False)

    dimes = db.relationship(
        "Dime", 
        backref="membre", 
        lazy=True, 
        cascade="all, delete-orphan"
    )


class Dime(db.Model):
    __tablename__ = "dimes"
    id = db.Column(db.Integer, primary_key=True)
    membre_id = db.Column(db.Integer, db.ForeignKey("membres.id"), nullable=False)  # ✅ corrigé
    date = db.Column(db.Date, nullable=False)
    montant = db.Column(db.Float, nullable=False)
    monnaie = db.Column(db.String(5), nullable=False)  # FC ou USD
    numero_recu = db.Column(db.String(20), unique=True, nullable=False)
    taux_change = db.Column(db.Float, nullable=True)  # Taux de change pour la conversion


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
