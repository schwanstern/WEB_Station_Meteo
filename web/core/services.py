from datetime import datetime


# Initial state
import os
import json
import socket
import requests
from django.db import connections
from django.db.utils import OperationalError
from core import influx_service

# Configuration
SYSTEM_DATA_DIR = "/app/system_data"
STATUS_FILE = os.path.join(SYSTEM_DATA_DIR, "system_status.json")
TRIGGER_FILE = os.path.join(SYSTEM_DATA_DIR, "trigger_update")


def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

def get_sensor_data(fallback_data=None):
    """
    Fetch sensor data from InfluxDB.
    If failure or empty, use fallback_data (SensorFallback model instance) if provided,
    otherwise default to zero/safe values.
    """
    real_data = influx_service.get_latest_data()
    
    if real_data:
        # DB Fields: humidite, luminosite, pression, speed, temperature, dir
        
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
        
    # Fallback / Mock Data from DB
    if fallback_data:
        return {
            "vent_vitesse": fallback_data.vent_vitesse,
            "vent_dir": fallback_data.vent_dir,
            "vent_angle": fallback_data.vent_angle,
            "temperature": fallback_data.temperature,
            "humidite": fallback_data.humidite,
            "pression": fallback_data.pression,
            "luminosite": fallback_data.luminosite,
        }

    # Ultimate fallback if no DB model exists yet
    return {
        "vent_vitesse": 0,
        "vent_dir": "N",
        "vent_angle": 0,
        "temperature": 0,
        "humidite": 0,
        "pression": 1013,
        "luminosite": 0,
    }

def get_alerts_logic(alert_rules=None):
    """Generate alerts based on sensor data and system state, using DB rules."""
    alerts = []
    # Note: get_sensor_data now requires fallback logic if we want to be safe,
    # but for alerts usually we check real data or we simply skip if no data.
    # calling get_sensor_data without fallback will return '0's as ultimate fallback
    data = get_sensor_data(fallback_data=None) 
    
    # Get system state (real)
    sys_state = get_system_state()
    
    mapping = {
        'wind_speed': data.get('vent_vitesse', 0),
        'temperature': data.get('temperature', 0),
        'humidity': data.get('humidite', 0),
        'pressure': data.get('pression', 0),
        # sys_update handled separately
    }

    if alert_rules:
        for rule in alert_rules:
            if not rule.is_active:
                continue
                
            if rule.metric == 'sys_update':
                 if sys_state.get("update_available", False):
                     alerts.append({
                        "titre": rule.name,
                        "message": rule.message,
                        "type": rule.alert_type,
                        "icon": rule.icon,
                        "action_link": "/gestion",
                     })
                 continue

            val = mapping.get(rule.metric)
            if val is not None:
                # Check min (exclusive)
                if rule.min_value is not None and val <= rule.min_value:
                    continue # Not triggered
                # Check max (exclusive)
                if rule.max_value is not None and val >= rule.max_value:
                    continue # Not triggered
                
                # If we are here, does it mean it IS triggered?
                # Usually alerts are: "If val > max then ALERT".
                # But here I defined min/max.
                # Let's assume the rule defines the "Danger Zone" or "Target Zone"?
                # Standard pattern: Alert if Value > Max OR Value < Min.
                # Let's adjust logic:
                # If rule has Max only: Trigger if Val > Max
                # If rule has Min only: Trigger if Val < Min
                # If rule has both: Trigger if Val < Min OR Val > Max (Out of range)
                
                triggered = False
                if rule.max_value is not None and val > rule.max_value:
                    triggered = True
                if rule.min_value is not None and val < rule.min_value:
                    triggered = True
                    
                if triggered:
                    alerts.append({
                        "titre": rule.name,
                        "message": rule.message.format(val=val), # Allow simple formatting
                        "type": rule.alert_type,
                        "icon": rule.icon,
                    })
    
    return alerts


def get_historical_data(period="1h"):
    """Generate historical data for the graph from InfluxDB."""
    
    # 1. Fetch real data
    points = influx_service.query_measurements("mqtt_consumer", duration=period)
    
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

    # 2. Fallback to Empty Data if no real data
    # (Previously random simulation, now removed to force real data usage)
    if period == "5m":
        labels = ["T-5", "T-4", "T-3", "T-2", "T-1", "Maintenant"]
        points_count = 6
        titre_periode = "Dernières 5 minutes"
    elif period == "15m":
        labels = ["T-15", "T-10", "T-5", "Maintenant"]
        points_count = 4 # Approx
        titre_periode = "Dernières 15 minutes"
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
        "vent": [0] * points_count,
        "temp": [0] * points_count,
        "hum": [0] * points_count,
        "press": [0] * points_count,
        "lux": [0] * points_count,
    }

    return {
        "datasets": datasets,
        "labels": labels,
        "period_label": titre_periode,
    }


def update_system():
    """Trigger the system update by creating the trigger file."""
    try:
        # Ensure dir exists (it should be mounted, but safe check)
        if not os.path.exists(SYSTEM_DATA_DIR):
            os.makedirs(SYSTEM_DATA_DIR, exist_ok=True)
            
        with open(TRIGGER_FILE, 'w') as f:
            f.write(f"Update triggered via Web UI at {datetime.now()}")
        return True
    except Exception as e:
        print(f"Error triggering update: {e}")
        return False


def get_system_state():
    """Retrieve current system state from shared JSON file."""
    state = {
        "update_available": False, 
        "last_update": "Inconnu",
        "updates_count": 0,
        "postgres": check_postgres(),
        "influxdb": check_influxdb(),
        "network": check_network(),
        "ttn": check_ttn_status()
    }
    
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                data = json.load(f)
                state["updates_count"] = data.get("updates_count", 0)
                state["last_update"] = data.get("last_check", "Inconnu")
                state["update_available"] = state["updates_count"] > 0
        except Exception as e:
            print(f"Error reading status file: {e}")
            
    return state

# --- Status Checks ---

def check_postgres():
    try:
        db_conn = connections['default']
        db_conn.cursor()
        return True
    except OperationalError:
        return False

def check_influxdb():
    # If influx_service has a health check, use it, else basic ping
    return influx_service.check_connection()

def check_network():
    # Check internal connection to nginx (proxy)
    try:
        # Resolve 'nginx_proxy' or just check google DNS 8.8.8.8 if allowed
        # Let's check internal first
        socket.gethostbyname("nginx_proxy")
        return True
    except:
        return False

def check_ttn_status():
    """Check if we received data recently (< 1h)."""
    data = influx_service.get_latest_data()
    if not data:
        return False
        
    last_time_str = data.get('time')
    if not last_time_str:
        return False
        
    try:
        # Parse ISO format from Influx
        last_time = datetime.strptime(last_time_str, "%Y-%m-%dT%H:%M:%SZ")
        delta = datetime.now() - last_time
        return delta.total_seconds() < 3600 # 1 hour
    except:
        return False
