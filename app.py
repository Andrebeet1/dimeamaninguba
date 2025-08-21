from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import logging
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash

# ==========================
# Initialisation Flask
# ==========================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secretkey123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dime.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================
# Modèles
# ==========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

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
    taux_change = db.Column(db.Float, nullable=True)  # Taux de change pour la conversion

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# ==========================
# Création automatique des tables
# ==========================
with app.app_context():
    db.create_all()
    logging.info("Tables créées avec succès !")

# ==========================
# Fonction pour calculer le temps écoulé
# ==========================
def time_ago(timestamp):
    now = datetime.utcnow()
    diff = now - timestamp

    if diff.total_seconds() < 60:
        return "Il y a quelques secondes"
    elif diff.total_seconds() < 3600:
        minutes = diff.seconds // 60
        return f"Il y a {minutes} minute{'s' if minutes != 1 else ''}"
    elif diff.total_seconds() < 86400:
        hours = diff.seconds // 3600
        return f"Il y a {hours} heure{'s' if hours != 1 else ''}"
    else:
        days = diff.days
        return f"Il y a {days} jour{'s' if days != 1 else ''}"

# ==========================
# Routes
# ==========================
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Connexion réussie !', 'success')
            return redirect(url_for('home'))
        flash('Nom d’utilisateur ou mot de passe incorrect.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Déconnexion réussie !', 'success')
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/ajouter_utilisateur', methods=['GET'])
def ajouter_utilisateur():
    with app.app_context():
        username = "Amaninguba"
        password = "amani4321"
        hashed_password = generate_password_hash(password)

        if User.query.filter_by(username=username).first() is None:
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return 'Utilisateur ajouté avec succès !'
        return 'L\'utilisateur existe déjà.', 400

@app.route('/ajouter_membre', methods=['GET', 'POST'])
def ajouter_membre():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        try:
            membre = Membre(
                nom=request.form['nom'],
                postnom=request.form['postnom'],
                date_naissance=datetime.strptime(request.form['date_naissance'], '%Y-%m-%d'),
                adresse=request.form['adresse'],
                telephone=request.form['telephone'],
                section=request.form['section']
            )
            db.session.add(membre)
            db.session.commit()
            flash('Membre ajouté avec succès !', 'success')
            return redirect(url_for('liste_membre'))
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du membre: {e}")
            flash('Erreur lors de l\'ajout du membre.', 'danger')
    return render_template('ajouter_membre.html')

@app.route('/liste_membre')
def liste_membre():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        membres = Membre.query.all()
        return render_template('liste_membre.html', membres=membres)
    except Exception as e:
        logging.error(f"Erreur lors de l'affichage des membres: {e}")
        flash('Erreur lors de l\'affichage des membres.', 'danger')
        return redirect(url_for('home'))

@app.route('/supprimer_membre/<int:membre_id>', methods=['POST'])
def supprimer_membre(membre_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        membre = Membre.query.get_or_404(membre_id)
        db.session.delete(membre)
        db.session.commit()
        flash('Membre supprimé avec succès !', 'success')
    except Exception as e:
        logging.error(f"Erreur lors de la suppression du membre: {e}")
        flash('Erreur lors de la suppression du membre.', 'danger')

    return redirect(url_for('liste_membre'))

@app.route('/enregistrer_dime', methods=['GET', 'POST'])
def enregistrer_dime():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    membres = Membre.query.all()
    if request.method == 'POST':
        try:
            membre_id = request.form['membre_id']
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            montant = float(request.form['montant'])
            monnaie = request.form['monnaie']
            taux_change = float(request.form['taux_change']) if monnaie == 'FC' else None

            prefix = date.strftime('%m%d')
            last_dime = Dime.query.order_by(Dime.id.desc()).first()
            last_num = (last_dime.id + 1) if last_dime else 1
            numero_recu = f"{prefix}#{last_num:04d}"

            dime = Dime(
                membre_id=membre_id,
                date=date,
                montant=montant,
                monnaie=monnaie,
                numero_recu=numero_recu,
                taux_change=taux_change
            )
            db.session.add(dime)
            db.session.commit()

            flash('Dime enregistrée avec succès !', 'success')
            return redirect(url_for('liste_dime'))
        except Exception as e:
            logging.error(f"Erreur lors de l'enregistrement de la dime: {e}")
            flash('Erreur lors de l\'enregistrement de la dime.', 'danger')
    
    return render_template('enregistrer_dime.html', membres=membres)

@app.route('/liste_dime')
def liste_dime():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        dimes = Dime.query.order_by(Dime.date.desc()).all()
        return render_template('liste_dime.html', dimes=dimes)
    except Exception as e:
        logging.error(f"Erreur lors de l'affichage des dîmes: {e}")
        flash('Erreur lors de l\'affichage des dîmes.', 'danger')
        return redirect(url_for('home'))

@app.route('/recu/<int:dime_id>')
def recu(dime_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        dime = Dime.query.options(joinedload(Dime.membre)).get_or_404(dime_id)
        return render_template('recu.html', dime=dime)
    except Exception as e:
        logging.error(f"Erreur lors de l'affichage du reçu: {e}")
        flash('Erreur lors de l\'affichage du reçu.', 'danger')
        return redirect(url_for('liste_dime'))

@app.route('/rapport_mensuel')
def rapport_mensuel():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        membres_count = Membre.query.count()
        dimes = Dime.query.all()

        total_fc = sum(d.montant for d in dimes if d.monnaie == 'FC')
        total_usd = sum(d.montant for d in dimes if d.monnaie == 'USD')

        # Conversion pour le total général en USD
        taux_change = 2000
        total_general_usd = total_usd + (total_fc / taux_change)

        logging.info(f"Membres: {membres_count}, Total FC: {total_fc}, Total USD: {total_usd}")

        return render_template('rapport_mensuel.html',
                               membres_count=membres_count,
                               total_fc=total_fc,
                               total_usd=total_usd,
                               total_general_usd=round(total_general_usd, 2))
    except Exception as e:
        logging.error(f"Erreur lors de l'affichage du rapport: {e}")
        flash('Erreur lors de l\'affichage du rapport.', 'danger')
        return redirect(url_for('home'))

@app.route('/notifications')
def notifications_view():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        notifications = Notification.query.order_by(Notification.date_created.desc()).all()
        return render_template('notifications.html', notifications=notifications, time_ago=time_ago)
    except Exception as e:
        logging.error(f"Erreur lors de l'affichage des notifications: {e}")
        flash('Erreur lors de l\'affichage des notifications.', 'danger')
        return redirect(url_for('home'))

@app.route('/rechercher_membre', methods=['GET'])
def rechercher_membre():
    nom = request.args.get('nom', '')
    if nom:
        membres = Membre.query.filter(Membre.nom.ilike(f'%{nom}%')).all()
        return jsonify([{'id': membre.id, 'nom': membre.nom, 'postnom': membre.postnom} for membre in membres])
    return jsonify([])

# ==========================
# Lancer l'application
# ==========================
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
