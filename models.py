from app import db

class Membre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    postnom = db.Column(db.String(50), nullable=False)

class Dime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_recu = db.Column(db.String(20), nullable=False)
    membre_id = db.Column(db.Integer, db.ForeignKey('membre.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    monnaie = db.Column(db.String(10), nullable=False)
