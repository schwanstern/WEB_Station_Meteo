from datetime import datetime
import random

# Initial state
SYSTEM_STATE = {"update_available": True, "last_update": "Jamais"}


from core import influx_service

def get_sensor_data():
    """Fetch sensor data from InfluxDB, fallback to mock if failure/empty."""
    real_data = influx_service.get_latest_data()
    
    if real_data:
        # DB Fields: humidite, luminosite, pression, speed, temperature, dir
        
        # Helper to safely float
        def safe_float(val):
            try:
                return float(val)
            except (ValueError, TypeError):
                return 0.0

        vent_vitesse = safe_float(real_data.get('speed', 0))
        angle = safe_float(real_data.get('dir', 0))
        
        # Helper to convert angle to cardinal text
        def angle_to_cardinal(deg):
            dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
            idx = int((deg + 22.5) / 45)
            # Ensure idx is positive
            return dirs[idx % 8]

        direction_texte = angle_to_cardinal(angle)
        
        return {
            "vent_vitesse": round(vent_vitesse, 1),
            "vent_dir": direction_texte,
            "vent_angle": angle,
            "temperature": round(safe_float(real_data.get('temperature', 0)), 1),
            "humidite": int(safe_float(real_data.get('humidite', 0))),
            "pression": int(safe_float(real_data.get('pression', 1013))),
            "luminosite": int(safe_float(real_data.get('luminosite', 0))),
        }
        
    # Fallback / Mock Data
    direction_texte = "S"
    mapping_direction = { "N": 0, "NE": 45, "E": 90, "SE": 135, "S": 180, "SW": 225, "W": 270, "NW": 315 }
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
                "action_link": "/gestion",
            }
        )

    return alerts


def get_historical_data(period="1h"):
    """Generate historical data for the graph from InfluxDB."""
    
    # 1. Fetch real data
    points = influx_service.query_measurements("ttn_uplink_student", duration=period)
    
    if points:
        labels = []
        datasets = {
            "vent": [], "temp": [], "hum": [], "press": [], "lux": []
        }
        
        for p in points:
            # Parse time
            dt_str = p.get('time', '')
            if dt_str:
                try:
                    # Influx returns ISO string. 
                    # If using 'influxdb' plain client, it might return string.
                    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")
                    # Ajout du jour/mois pour visibilité sur plusieurs jours
                    labels.append(dt.strftime("%d/%m %H:%M"))
                except:
                     labels.append(dt_str)
            else:
                labels.append("")

            # Helper to safely float
            def safe_float(val):
                try:
                    return float(val)
                except (ValueError, TypeError):
                    return 0.0

            # Map fields: speed -> vent
            datasets["vent"].append(safe_float(p.get('speed', 0)))
            datasets["temp"].append(safe_float(p.get('temperature', 0)))
            datasets["hum"].append(safe_float(p.get('humidite', 0)))
            datasets["press"].append(safe_float(p.get('pression', 0)))
            datasets["lux"].append(safe_float(p.get('luminosite', 0)))
            
        titre_periode = f"Données réelles ({period})"

        return {
            "datasets": datasets,
            "labels": labels,
            "period_label": titre_periode,
        }

    # 2. Fallback to Random Mock Data if no real data
    if period == "5m":
        labels = ["T-5", "T-4", "T-3", "T-2", "T-1", "Maintenant"]
        points_count = 6
        titre_periode = "Dernières 5 minutes"
    elif period == "24h":
        labels = [f"{i}h" for i in range(0, 25, 2)]
        points_count = 13
        titre_periode = "Dernières 24 heures"
    elif period == "7d":
        labels = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        points_count = 7
        titre_periode = "7 derniers jours"
    else:  # Default '1h'
        labels = ["0min", "10min", "20min", "30min", "40min", "50min", "60min"]
        points_count = 7
        titre_periode = "Dernière heure"

    datasets = {
        "vent": [random.randint(5, 30) for _ in range(points_count)],
        "temp": [random.randint(15, 25) for _ in range(points_count)],
        "hum": [random.randint(40, 80) for _ in range(points_count)],
        "press": [random.randint(1010, 1020) for _ in range(points_count)],
        "lux": [random.randint(0, 1000) for _ in range(points_count)],
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
