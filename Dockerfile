FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installation des dépendances système de base
RUN apt-get update && apt-get install -y netcat-openbsd gcc && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copie du code source
COPY . /app/

# Port exposé
EXPOSE 8000

# Commande de lancement (sera surchargée par docker-compose mais utile par défaut)
CMD ["gunicorn", "ton_projet.wsgi:application", "--bind", "0.0.0.0:8000"]