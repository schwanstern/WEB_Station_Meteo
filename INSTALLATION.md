# 🚀 Guide d'Installation - Station Météo

Ce guide détaille les étapes pour installer et déployer l'application Station Météo sur votre serveur.

## 1. Récupération du Projet

Vous devez disposer de **Git** sur votre machine.

```bash
# Installation de Git (si nécessaire)
sudo apt-get update && sudo apt-get install -y git

# Clonage du projet
cd /home/meteo
git clone git@github.com:schwanstern/WEB_Station_Meteo.git
cd WEB_Station_Meteo
```

## 2. Installation des Pré-requis (Docker)

Une fois le projet cloné, vous pouvez utiliser le script inclus pour installer Docker et Docker Compose automatiquement.

```bash
chmod +x install_prerequisites.sh
sudo ./install_prerequisites.sh
```

**⚠️ Important :** Une fois l'installation terminée, **déconnectez-vous et reconnectez-vous** à votre session pour que les permissions Docker soient prises en compte (ou lancez `newgrp docker`).

## 3. Configuration de l'Environnement

Le projet nécessite un fichier `.env`.

```bash
cp .env.example .env
nano .env
```

Remplissez les variables (voir [CONFIGURATION.md](./CONFIGURATION.md)).

## 4. Démarrage de la Station

Lancer l'application :

```bash
docker compose up -d
```

Vérifier que tout tourne :

```bash
docker compose ps
```

## 5. Installation du Service (Démarrage Automatique)

Pour que la station démarre avec le serveur (voir détails dans le fichier `station-meteo.service`) :

```bash
sudo cp station-meteo.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable station-meteo.service
sudo systemctl start station-meteo.service
```
