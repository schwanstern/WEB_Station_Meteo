FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installation des dépendances système de base
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copie du code source
COPY . /app/

# Copie du script d'entrypoint
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Port exposé
EXPOSE 8000

# Définition de l'entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Commande par défaut (passée à l'entrypoint via "$@")
CMD ["gunicorn", "station_meteo.wsgi:application", "--bind", "0.0.0.0:8000"]