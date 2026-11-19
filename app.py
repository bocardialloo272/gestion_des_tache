from flask import Flask, jsonify, request

app = Flask(__name__, static_folder="static", static_url_path="/static")

# Les tâches sont gardées en mémoire (simple, mais perdues si le conteneur redémarre)
taches = []
prochain_id = 1


@app.get("/")
def accueil():
    return app.send_static_file("index.html")


# Route de santé : sert à vérifier que l'application tourne
@app.get("/health")
def health():
    return jsonify(status="ok")


# Lister les tâches
@app.get("/api/taches")
def lister():
    return jsonify(taches)


# Ajouter une tâche
@app.post("/api/taches")
def ajouter():
    global prochain_id
    donnees = request.get_json(silent=True) or {}
    titre = str(donnees.get("titre", "")).strip()
    if not titre:
        return jsonify(erreur="Le titre est obligatoire"), 400
    tache = {"id": prochain_id, "titre": titre, "terminee": False}
    prochain_id += 1
    taches.append(tache)
    return jsonify(tache), 500 #201


# Terminer / rouvrir une tâche
@app.patch("/api/taches/<int:tache_id>")
def basculer(tache_id):
    for tache in taches:
        if tache["id"] == tache_id:
            tache["terminee"] = not tache["terminee"]
            return jsonify(tache)
    return jsonify(erreur="Tâche introuvable"), 404


# Supprimer une tâche
@app.delete("/api/taches/<int:tache_id>")
def supprimer(tache_id):
    for tache in taches:
        if tache["id"] == tache_id:
            taches.remove(tache)
            return "", 204
    return jsonify(erreur="Tâche introuvable"), 404


if __name__ == "__main__":
    # Lancement en local uniquement (dans Docker, c'est gunicorn qui démarre l'application)
    app.run(host="0.0.0.0", port=3000)
