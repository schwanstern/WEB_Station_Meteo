# Gestion du Serveur (Orange Pi)

Ce document explique comment installer et gérer le service systemd pour l'application Station Météo sur votre Orange Pi.

## ✅ Pré-requis

- Avoir cloné le projet dans `/home/meteo/WEB_Station_Meteo`.
- Avoir un fichier `.env` configuré à la racine.
- Avoir les permissions `sudo`.

## 🚀 Installation du Service (Démarrage Automatique)

Cette étape permet de lancer l'application automatiquement au démarrage de la carte.

1.  **Copier le fichier de service** :
    ```bash
    sudo cp station-meteo.service /etc/systemd/system/
    ```

2.  **Recharger systemd** (pour qu'il prenne en compte le nouveau fichier) :
    ```bash
    sudo systemctl daemon-reload
    ```

3.  **Activer le service au démarrage** :
    ```bash
    sudo systemctl enable station-meteo.service
    ```

4.  **Démarrer le service immédiatement** :
    ```bash
    sudo systemctl start station-meteo.service
    ```

## 🛠 Commandes de Gestion

Voici les commandes pour gérer l'application au quotidien :

| Action | Commande |
| :--- | :--- |
| **Démarrer** | `sudo systemctl start station-meteo` |
| **Arrêter** | `sudo systemctl stop station-meteo` |
| **Redémarrer** | `sudo systemctl restart station-meteo` |
| **Vérifier l'état** | `sudo systemctl status station-meteo` |
| **Voir les logs (Systemd)** | `sudo journalctl -u station-meteo -f` |

## 🐳 Gestion Docker (Avancé)

Si vous devez intervenir directement sur les conteneurs (ex: reconstruire après une modification du Dockerfile) :

```bash
# Se placer dans le dossier
cd /home/meteo/WEB_Station_Meteo

# Vérifier l'état des conteneurs
docker compose ps

# Reconstruire l'image web (nécessaire si modification python/Dockerfile)
docker compose build web

# Voir les logs d'un conteneur spécifique (ex: web)
docker compose logs -f web
```

## ⚠️ Dépannage Rapide

**Le service échoue avec l'erreur `203/EXEC`** :
- Vérifiez que `docker compose` est bien installé et accessible (`/usr/bin/docker`).

**Le service échoue avec l'erreur `200/CHDIR`** :
- Vérifiez que le dossier `/home/meteo/WEB_Station_Meteo` existe bien.

**L'application web redémarre en boucle (unhealthy)** :
- Vérifiez les logs : `docker compose logs web`
- Assurez-vous d'avoir reconstruit l'image si vous venez de faire une mise à jour : `docker compose build web`
