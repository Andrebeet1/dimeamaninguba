from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from models import Membre, Dime

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/membres', methods=['GET', 'POST'])
def liste_membre():
    if request.method == 'POST':
        nom = request.form['nom']
        postnom = request.form['postnom']
        new_membre = Membre(nom=nom, postnom=postnom)
        db.session.add(new_membre)
        db.session.commit()
        flash('Membre ajouté avec succès!', 'success')
        return redirect(url_for('liste_membre'))
    
    membres = Membre.query.all()
    return render_template('liste_membre.html', membres=membres)

@app.route('/ajouter_membre')
def ajouter_membre():
    return render_template('ajouter_membre.html')

@app.route('/dimes', methods=['GET', 'POST'])
def enregistrer_dime():
    if request.method == 'POST':
        numero_recu = request.form['numero_recu']
        membre_id = request.form['membre_id']
        montant = float(request.form['montant'])
        monnaie = request.form['monnaie']
        new_dime = Dime(numero_recu=numero_recu, membre_id=membre_id, montant=montant, monnaie=monnaie)
        db.session.add(new_dime)
        db.session.commit()
        flash('Dîme enregistrée avec succès!', 'success')
        return redirect(url_for('enregistrer_dime'))
    
    membres = Membre.query.all()
    return render_template('enregistrer_dime.html', membres=membres)

@app.route('/liste_dime')
def liste_dime():
    dimes = Dime.query.all()
    return render_template('liste_dime.html', dimes=dimes)

@app.route('/recu')
def recu():
    return render_template('reçu.html')

@app.route('/rapport')
def rapport_mensuel():
    return render_template('rapport_mensuel.html')

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

if __name__ == '__main__':
    app.run(debug=True)
