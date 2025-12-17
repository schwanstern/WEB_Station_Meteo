from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cle_secrete_pour_flash' # Nécessaire pour les petits messages de confirmation

# --- Variables d'état (Simulation) ---
# Dans un vrai projet, cela viendrait d'une base de données ou d'un fichier config
SYSTEM_STATE = {
    "update_available": True,  # Une mise à jour est dispo par défaut
    "last_update": "Jamais"
}

# Dans app.py

def get_sensor_data():
    # Simulation de la direction (change ça pour tester !)
    direction_texte = "S" 
    
    # Petit dictionnaire pour convertir le texte en degrés pour la boussole
    mapping_direction = {
        "N": 0, "NE": 45, "E": 90, "SE": 135,
        "S": 180, "SW": 225, "W": 270, "NW": 315
    }
    
    # On récupère l'angle (0 par défaut si inconnu)
    angle = mapping_direction.get(direction_texte, 0)

    return {
        "vent_vitesse": 15,    
        "vent_dir": direction_texte, # Le texte (ex: "NE")
        "vent_angle": angle,         # L'angle (ex: 45) -> NOUVEAU
        "temperature": 22.5,   
        "humidite": 60,        
        "pression": 1013,      
        "luminosite": 750      
    }

def get_alerts():
    """Génère la liste des messages pour l'accueil"""
    alerts = []
    data = get_sensor_data()

    # 1. Alerte Vent Fort
    if data['vent_vitesse'] > 15:
        alerts.append({
            "titre": "VENT FORT",
            "message": f"La vitesse du vent est de {data['vent_vitesse']} km/h. Sécurisez le matériel.",
            "type": "danger",  # Rouge
            "icon": "bi-exclamation-triangle-fill"
        })
    else:
        # Message informatif si tout va bien
        alerts.append({
            "titre": "Météo Calme",
            "message": "Conditions normales. Vitesse du vent faible.",
            "type": "success", # Vert
            "icon": "bi-check-circle-fill"
        })

    # 2. Alerte Mise à jour Système
    if SYSTEM_STATE['update_available']:
        alerts.append({
            "titre": "MISE À JOUR DISPONIBLE",
            "message": "Une nouvelle version du système est prête.",
            "type": "primary", # Bleu
            "icon": "bi-cloud-arrow-down-fill",
            "action_link": "/gestion" # Lien vers la page pour régler ça
        })

    return alerts

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # On vérifie quel formulaire a été envoyé grâce au champ caché 'action'
        action = request.form.get('action')

        if action == 'login':
            # Logique de connexion (Simulée)
            user = request.form.get('user')
            password = request.form.get('mdp')
            # Ici tu vérifieras dans InfluxDB ou une autre base SQL
            if user and password: 
                return redirect(url_for('accueil'))
            else:
                flash("Identifiants incorrects", "danger")

        elif action == 'register':
            # Logique d'inscription (Simulée)
            new_user = request.form.get('new_user')
            # Ici tu enregistrerais l'utilisateur
            flash(f"Compte créé pour {new_user} ! Connectez-vous.", "success")
            # On ne redirige pas pour laisser l'utilisateur se connecter
        
        elif action == 'reset_password':
            # Logique mot de passe oublié (Simulée)
            email = request.form.get('email')
            flash(f"Un lien de réinitialisation a été envoyé à {email} (Simulation).", "info")
            
    return render_template('login.html')

@app.route('/accueil')
def accueil():
    # On récupère les alertes générées par Python
    mes_alertes = get_alerts()
    return render_template('index.html', 
                           time=datetime.now().strftime("%H:%M"), 
                           alerts=mes_alertes) # On passe la liste au HTML

@app.route('/gestion', methods=['GET', 'POST'])
def gestion():
    if request.method == 'POST':
        # Si on clique sur le bouton "Mettre à jour"
        if 'do_update' in request.form:
            SYSTEM_STATE['update_available'] = False
            SYSTEM_STATE['last_update'] = datetime.now().strftime("%d/%m/%Y à %H:%M")
            # flash envoie un message temporaire à la page suivante
            flash("Mise à jour effectuée avec succès !", "success")
            
    return render_template('gestion.html', state=SYSTEM_STATE)

@app.route('/apercu')
def apercu():
    return render_template('apercu.html', data=get_sensor_data())

@app.route('/graph')
def graph():
    # Données fictives pour le graph
    data = [5, 12, 19, 15, 22, 28, 24, 20]
    return render_template('graph.html', data=data)

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True, port=5501)