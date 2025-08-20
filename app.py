from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import logging

# ==========================
# Initialisation Flask
# ==========================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secretkey123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///dime.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================
# Modèles
# ==========================
class Membre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    postnom = db.Column(db.String(50), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    adresse = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(20), nullable=False)
    dimes = db.relationship('Dime', backref='membre', lazy=True)

class Dime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    membre_id = db.Column(db.Integer, db.ForeignKey('membre.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    montant = db.Column(db.Float, nullable=False)
    monnaie = db.Column(db.String(5), nullable=False)  # FC ou USD
    numero_recu = db.Column(db.String(20), unique=True, nullable=False)

# ==========================
# Création automatique des tables
# ==========================
@app.before_serving
def create_tables():
    db.create_all()
    logging.info("Tables créées avec succès !")

# ==========================
# Routes classiques
# ==========================
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/ajouter_membre', methods=['GET', 'POST'])
def ajouter_membre():
    if request.method == 'POST':
        try:
            nom = request.form['nom']
            postnom = request.form['postnom']
            date_naissance = datetime.strptime(request.form['date_naissance'], '%Y-%m-%d')
            adresse = request.form['adresse']
            telephone = request.form['telephone']
            section = request.form['section']
            
            membre = Membre(
                nom=nom,
                postnom=postnom,
                date_naissance=date_naissance,
                adresse=adresse,
                telephone=telephone,
                section=section
            )
            db.session.add(membre)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            logging.error(e)
            return jsonify({'success': False, 'message': str(e)})
    return render_template('ajouter_membre.html')

@app.route('/liste_membre')
def liste_membre():
    try:
        membres = Membre.query.all()
        return render_template('liste_membre.html', membres=membres)
    except Exception as e:
        logging.error(e)
        return "Erreur lors de l'affichage des membres : " + str(e), 500

@app.route('/enregistrer_dime', methods=['GET', 'POST'])
def enregistrer_dime():
    membres = Membre.query.all()
    if request.method == 'POST':
        try:
            membre_id = request.form['membre_id']
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            montant = float(request.form['montant'])
            monnaie = request.form['monnaie']

            prefix = date.strftime('%m%d')
            last_dime = Dime.query.order_by(Dime.id.desc()).first()
            last_num = int(last_dime.id) + 1 if last_dime else 1
            numero_recu = f"{prefix}#{last_num:04d}"

            dime = Dime(
                membre_id=membre_id,
                date=date,
                montant=montant,
                monnaie=monnaie,
                numero_recu=numero_recu
            )
            db.session.add(dime)
            db.session.flush()
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            logging.error(e)
            return jsonify({'success': False, 'message': str(e)})
    return render_template('enregistrer_dime.html', membres=membres)

@app.route('/liste_dime')
def liste_dime():
    try:
        dimes = Dime.query.order_by(Dime.date.desc()).all()
        return render_template('liste_dime.html', dimes=dimes)
    except Exception as e:
        logging.error(e)
        return "Erreur lors de l'affichage des dîmes : " + str(e), 500

@app.route('/recu/<int:dime_id>')
def recu(dime_id):
    try:
        dime = Dime.query.get_or_404(dime_id)
        return render_template('recu.html', dime=dime)
    except Exception as e:
        logging.error(e)
        return "Erreur lors de l'affichage du reçu : " + str(e), 500

@app.route('/rapport_mensuel')
def rapport_mensuel():
    try:
        membres_count = Membre.query.count()
        dimes = Dime.query.all()
        total_fc = sum(d.montant for d in dimes if d.monnaie == 'FC')
        total_usd = sum(d.montant for d in dimes if d.monnaie == 'USD')
        taux_change = 2000
        total_general_usd = total_usd + total_fc / taux_change
        return render_template('rapport_mensuel.html',
                               membres_count=membres_count,
                               total_fc=total_fc,
                               total_usd=total_usd,
                               total_general_usd=round(total_general_usd, 2))
    except Exception as e:
        logging.error(e)
        return "Erreur lors de l'affichage du rapport : " + str(e), 500

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

# ==========================
# Lancer l'application
# ==========================
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
