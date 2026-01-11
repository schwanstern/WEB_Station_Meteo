# 🛠 Guide de Gestion - Station Météo

Ce document regroupe les commandes utiles pour gérer votre station météo au quotidien.

## 🕹 Gestion du Service (Systemd)

Si vous avez installé le service systemd, utilisez ces commandes pour piloter l'application globale.

| Action | Commande | Description |
| :--- | :--- | :--- |
| **Démarrer** | `sudo systemctl start station-meteo` | Lance tous les conteneurs. |
| **Arrêter** | `sudo systemctl stop station-meteo` | Arrête proprement tous les conteneurs. |
| **Redémarrer** | `sudo systemctl restart station-meteo` | Redémarre l'ensemble de la stack. |
| **État** | `sudo systemctl status station-meteo` | Vérifie si le service est actif. |
| **Logs Système** | `sudo journalctl -u station-meteo -f` | Affiche les logs du démon systemd. |

## 🐳 Gestion des Conteneurs (Docker)

Pour des actions plus précises (logs d'un service spécifique, mises à jour), utilisez Docker Compose directement dans le dossier du projet.

**Se placer dans le dossier :**
```bash
cd /home/meteo/WEB_Station_Meteo
```

### Voir les Logs

*   **Tous les logs :**
    ```bash
    docker compose logs -f
    ```
*   **Logs d'un service spécifique** (ex: `web`, `telegraf`, `influxdb`) :
    ```bash
    docker compose logs -f web
    ```

### Mettre à Jour l'Application

Si une nouvelle version de l'image Docker est disponible sur le registre :

1.  **Télécharger la nouvelle image :**
    ```bash
    docker compose pull
    ```
2.  **Redémarrer les conteneurs :**
    ```bash
    docker compose up -d
    ```
    *(Docker va recréer uniquement les conteneurs mis à jour)*

### Maintenance de la Base de Données

Accéder au shell du conteneur DB :
```bash
docker compose exec db psql -U votre_user -d votre_db
```

### Vérifier l'état de santé

```bash
docker compose ps
```
La colonne `STATUS` doit indiquer `(healthy)` pour les services critiques.
