# Gestion des tâches

Application web simple (Python + Flask) pour le projet CI/CD avec GitHub Actions.

## Lancer en local
    pip install -r requirements-dev.txt
    python app.py        # http://localhost:3000
    pytest

## Avec Docker
    docker build -t gestion-taches .
    docker run -d -p 8080:3000 gestion-taches    # http://localhost:8080

## Secrets GitHub à créer (Settings > Secrets and variables > Actions)
- DOCKERHUB_USERNAME : ton nom d'utilisateur Docker Hub
- DOCKERHUB_TOKEN : un jeton d'accès Docker Hub (pas ton mot de passe)
