# ⚙️ Guide de Configuration - Station Météo

La configuration de la station météo repose principalement sur le fichier `.env` et quelques fichiers de configuration spécifiques.

## 1. Variables d'Environnement (.env)

Le fichier `.env` à la racine est le cœur de la configuration. Il ne doit **JAMAIS** être commité sur Git s'il contient des mots de passe réels.

### Base de Données (PostgreSQL)
Ces variables configurent l'accès à la base de données relationnelle.

*   `POSTGRES_DB`: Nom de la base de données.
*   `POSTGRES_USER`: Utilisateur de la base de données.
*   `POSTGRES_PASSWORD`: Mot de passe de la base de données.
*   `POSTGRES_HOST`: Nom du service docker (généralement `db`).
*   `POSTGRES_PORT`: Port (par défaut `5432`).

### InfluxDB (Base de données Séries Temporelles)
Configuration pour InfluxDB v2.

*   `DOCKER_INFLUXDB_INIT_MODE`: Mode d'initialisation (ex: `setup`).
*   `DOCKER_INFLUXDB_INIT_USERNAME`: Nom d'utilisateur admin initial.
*   `DOCKER_INFLUXDB_INIT_PASSWORD`: Mot de passe admin initial.
*   `DOCKER_INFLUXDB_INIT_ORG`: Organisation InfluxDB.
*   `DOCKER_INFLUXDB_INIT_BUCKET`: Bucket par défaut pour les données.
*   `INFLUX_TOKEN`: **Token Admin** (très important, doit être sécurisé). Utilisé par Telegraf et le Web pour écrire/lire les données.

### The Things Network (TTN) via Telegraf
Configuration pour la récupération des données MQTT depuis TTN.

*   `TTN_BROKER`: Adresse du broker (ex: `eu1.cloud.thethings.network:1883`).
*   `TTN_APP_ID`: ID de l'application TTN (Username MQTT).
*   `TTN_API_KEY`: Clé API TTN (Password MQTT).

### Django (Web)
*   `SECRET_KEY`: Clé secrète Django (générez une chaîne aléatoire longue).
*   `DEBUG`: Mettre à `0` ou `False` en production.
*   `ALLOWED_HOSTS`: Liste des domaines autorisés (ex: `mon-site.com,localhost`).

### Cloudflare Tunnel
*   `CF_TUNNEL_TOKEN`: Token d'authentification pour le tunnel Cloudflare.

---

## 2. Configuration Telegraf (`telegraf/telegraf.conf`)

Ce fichier configure l'agent de collecte de données.
*   **Input MQTT** : Souscrit au topic `v3/+/devices/+/up` pour recevoir les données des capteurs LoRaWAN.
*   **Output InfluxDB_v2** : Envoie les données vers le conteneur `influxdb` en utilisant le token défini dans les variables d'environnement.

## 3. Configuration Nginx (`nginx/default.conf`)

Nginx agit comme reverse proxy.
*   Sert les fichiers statiques (`/static/`) directement pour la performance.
*   Redirige le reste du trafic vers le conteneur `web` (Gunicorn/Django).
*   Gère les timeouts et les headers de proxy.

## 4. Configuration Docker Compose

Le fichier `docker-compose.yml` orchestre les services :
*   **Réseau** : Tous les services communiquent via `internal_net`.
*   **Redémarrage** : `restart: always` assure que les services redémarrent en cas de crash.
*   **Limites** : Des limites de mémoire sont définies pour éviter de saturer le serveur (ex: Orange Pi).
