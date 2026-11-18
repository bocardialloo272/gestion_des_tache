# Image de base légère avec Python
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# On installe d'abord les dépendances (meilleur cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Puis on copie le code de l'application
COPY . .

# On n'exécute pas l'application en administrateur
RUN useradd --create-home appuser
USER appuser

EXPOSE 3000

# 1 seul worker : les tâches sont gardées en mémoire, un 2e worker aurait sa propre liste
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "1", "--threads", "4", "app:app"]
