from datetime import datetime
import random

# Initial state
SYSTEM_STATE = {"update_available": True, "last_update": "Jamais"}


def get_sensor_data():
    """Simulate fetching sensor data."""
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
        "vent_vitesse": 25,
        "vent_dir": direction_texte,
        "vent_angle": angle,
        "temperature": 22.5,
        "humidite": 60,
        "pression": 1013,
        "luminosite": 750,
    }


def get_alerts_logic():
    """Generate alerts based on sensor data and system state."""
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
                "action_link": "/gestion",  # Will need adjustment if URL name changes, but keeping for now
            }
        )

    return alerts


def get_historical_data(period="1h"):
    """Generate historical data for the graph."""
    if period == "5m":
        labels = ["T-5", "T-4", "T-3", "T-2", "T-1", "Maintenant"]
        points = 6
        titre_periode = "Dernières 5 minutes"
    elif period == "24h":
        labels = [f"{i}h" for i in range(0, 25, 2)]
        points = 13
        titre_periode = "Dernières 24 heures"
    elif period == "7d":
        labels = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        points = 7
        titre_periode = "7 derniers jours"
    else:  # Default '1h'
        labels = ["0min", "10min", "20min", "30min", "40min", "50min", "60min"]
        points = 7
        titre_periode = "Dernière heure"

    datasets = {
        "vent": [random.randint(5, 30) for _ in range(points)],
        "temp": [random.randint(15, 25) for _ in range(points)],
        "hum": [random.randint(40, 80) for _ in range(points)],
        "press": [random.randint(1010, 1020) for _ in range(points)],
        "lux": [random.randint(0, 1000) for _ in range(points)],
    }

    return {
        "datasets": datasets,
        "labels": labels,
        "period_label": titre_periode,
    }


def update_system():
    """Update the system state."""
    SYSTEM_STATE["update_available"] = False
    SYSTEM_STATE["last_update"] = datetime.now().strftime("%d/%m/%Y à %H:%M")
    return True


def get_system_state():
    """Retrieve current system state."""
    return SYSTEM_STATE
