#!/bin/bash

# Script d'installation des pré-requis pour la Station Météo
# Compatible : Debian, Ubuntu, Raspbian, Armbian

set -e

# Vérification des droits root
if [ "$EUID" -ne 0 ]
  then echo "❌ Veuillez lancer ce script avec sudo ou en tant que root."
  exit 1
fi

echo "🚀 Mise à jour du système..."
apt-get update && apt-get upgrade -y

echo "📦 Installation de Git, Curl et autres outils..."
apt-get install -y git curl wget ca-certificates gnupg lsbu-release

# Installation de Docker
if command -v docker &> /dev/null
then
    echo "✅ Docker est déjà installé."
else
    echo "🐳 Installation de Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# Démarrage de Docker
systemctl enable docker
systemctl start docker

# Ajout de l'utilisateur courant au groupe docker
# Si le script est lancé avec sudo, SUDO_USER contient le nom de l'utilisateur réel
REAL_USER=${SUDO_USER:-$USER}

if [ "$REAL_USER" != "root" ]; then
    echo "👤 Ajout de l'utilisateur $REAL_USER au groupe docker..."
    usermod -aG docker "$REAL_USER"
    echo "⚠️  NOTE : Vous devrez vous déconnecter et reconnecter pour que le groupe docker soit pris en compte."
else
    echo "⚠️  ATTENTION : Vous exécutez tout en root. Pensez à ajouter votre utilisateur normal au groupe docker si nécessaire."
fi

echo "✅ Installation terminée !"
echo "Versions installées :"
git --version
docker --version
docker compose version

echo "➡️  Vous pouvez maintenant passer à la suite de l'installation."
