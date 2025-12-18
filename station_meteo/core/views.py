from datetime import datetime

from django.contrib import messages  # Remplacement de flash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

# --- 1. Tes Variables & Fonctions (Copiées-collées de Flask) ---

# Note : Dans un vrai Django, ça irait dans models.py (Base de données)
# Mais pour l'instant, on garde ta logique telle quelle.
SYSTEM_STATE = {"update_available": True, "last_update": "Jamais"}


def get_sensor_data():
    direction_texte = "S"
    mapping_direction = {
        "N": 0,
        "NE": 45,
        "E": 90,
        "SE": 135,
        "S": 180,
        "SW": 225,
        "W": 270,
        "NW": 315,
    }
    angle = mapping_direction.get(direction_texte, 0)

    return {
        "vent_vitesse": 15,
        "vent_dir": direction_texte,
        "vent_angle": angle,
        "temperature": 22.5,
        "humidite": 60,
        "pression": 1013,
        "luminosite": 750,
    }


def get_alerts_logic():  # J'ai renommé légèrement pour éviter les confusions
    alerts = []
    data = get_sensor_data()

    if data["vent_vitesse"] > 15:
        alerts.append(
            {
                "titre": "VENT FORT",
                "message": f"La vitesse du vent est de {data['vent_vitesse']} km/h.",
                "type": "danger",
                "icon": "bi-exclamation-triangle-fill",
            }
        )
    else:
        alerts.append(
            {
                "titre": "Météo Calme",
                "message": "Conditions normales.",
                "type": "success",
                "icon": "bi-check-circle-fill",
            }
        )

    if SYSTEM_STATE["update_available"]:
        alerts.append(
            {
                "titre": "MISE À JOUR DISPONIBLE",
                "message": "Une nouvelle version est prête.",
                "type": "primary",
                "icon": "bi-cloud-arrow-down-fill",
                "action_link": "/gestion",  # Attention: on changera ça plus tard avec les URLs Django
            }
        )

    return alerts


# --- 2. Tes Routes converties en Vues Django ---


def root(request):
    if request.user.is_authenticated:
        return redirect("accueil")
    else:
        return redirect("login")


def login_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "login":
            # On récupère le champ unique (qui peut être email ou pseudo)
            saisie_identifiant = request.POST.get("identifiant")
            mot_de_passe = request.POST.get("mdp")

            username_to_login = saisie_identifiant

            # --- LOGIQUE EMAIL ---
            # Si la saisie contient '@', on suppose que c'est un email
            if "@" in saisie_identifiant:
                try:
                    # On cherche l'utilisateur qui possède cet email
                    user_obj = User.objects.get(email=saisie_identifiant)
                    # On récupère son vrai pseudo pour Django
                    username_to_login = user_obj.username
                except User.DoesNotExist:
                    # Si l'email n'existe pas, on laisse faire authenticate qui échouera
                    pass

            # On authentifie avec le pseudo trouvé (ou la saisie directe)
            user = authenticate(
                request, username=username_to_login, password=mot_de_passe
            )

            if user is not None:
                login(request, user)
                return redirect("accueil")
            else:
                messages.error(request, "Email/Utilisateur ou mot de passe incorrect")

    return render(request, "login.html")


def accueil(request):
    mes_alertes = get_alerts_logic()
    context = {"time": datetime.now().strftime("%H:%M"), "alerts": mes_alertes}
    return render(request, "index.html", context)


def gestion(request):
    if request.method == "POST":
        if "do_update" in request.POST:
            SYSTEM_STATE["update_available"] = False
            SYSTEM_STATE["last_update"] = datetime.now().strftime("%d/%m/%Y à %H:%M")
            messages.success(request, "Mise à jour effectuée avec succès !")

    return render(request, "gestion.html", {"state": SYSTEM_STATE})


def apercu(request):
    return render(request, "apercu.html", {"data": get_sensor_data()})


def graph(request):
    data = [5, 12, 19, 15, 22, 28, 24, 20]
    return render(request, "graph.html", {"data": data})


def settings(request):
    return render(request, "settings.html")


def logout_view(request):
    logout(request)  # Détruit la session
    messages.success(request, "Vous avez été déconnecté.")
    return redirect("login")
