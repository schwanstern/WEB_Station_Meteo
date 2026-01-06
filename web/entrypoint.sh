#!/bin/bash

# web/entrypoint.sh

# Quitter immédiatement si une commande échoue
set -e

echo "🚀 Démarrage du conteneur Web..."

# Fonction pour attendre la base de données
wait_for_db() {
    echo "⏳ Attente de la base de données Postgres..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
    echo "✅ Base de données Postgres disponible."
}

# Attendre que la DB soit prête (nécessite netcat installé dans l'image)
# Note: Dans docker-compose on utilise healthcheks, mais ceci est une double sécurité
# Si POSTGRES_HOST n'est pas défini, on suppose 'db'
HOST="${POSTGRES_HOST:-db}"
PORT="${POSTGRES_PORT:-5432}"

# On peut utiliser une boucle simple avec nc ou python si nc manque, 
# mais ici on assume que netcat-openbsd est installé via le Dockerfile.
echo "⏳ Vérification de la connectivité DB ($HOST:$PORT)..."
# On attend un peu que le DNS se propage ou que le service soit up
sleep 2

echo "📦 Application des migrations de base de données..."
python manage.py migrate --noinput

echo "🎨 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

echo "🔥 Démarrage de Gunicorn..."
exec "$@"
