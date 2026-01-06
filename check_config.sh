#!/bin/bash

# check_config.sh
# Vérifie que la configuration est présente avant de lancer quoi que ce soit.

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "🔍 Vérification de la configuration..."

if [ ! -f .env ]; then
    echo -e "${RED}❌ Erreur : Le fichier .env est manquant !${NC}"
    echo "Veuillez copier .env.example vers .env et remplir les variables."
    exit 1
fi

# Liste des variables critiques
REQUIRED_VARS=("POSTGRES_DB" "POSTGRES_USER" "POSTGRES_PASSWORD" "INFLUX_TOKEN" "TTN_API_KEY")

MISSING=0
for VAR in "${REQUIRED_VARS[@]}"; do
    if ! grep -q "^${VAR}=" .env; then
        echo -e "${RED}❌ Erreur : La variable ${VAR} est manquante dans .env${NC}"
        MISSING=1
    fi
done

if [ $MISSING -eq 1 ]; then
    echo "Configuration incomplète. Arrêt."
    exit 1
fi

echo -e "${GREEN}✅ Configuration validée.${NC}"
exit 0
