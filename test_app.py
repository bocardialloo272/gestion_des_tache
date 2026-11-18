from app import app


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health_repond_ok():
    r = client().get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_ajouter_puis_lister_une_tache():
    c = client()
    r = c.post("/api/taches", json={"titre": "Réviser l'exposé"})
    assert r.status_code == 201
    liste = c.get("/api/taches").get_json()
    assert any(t["titre"] == "Réviser l'exposé" for t in liste)


def test_titre_vide_refuse():
    r = client().post("/api/taches", json={"titre": "   "})
    assert r.status_code == 400


def test_terminer_puis_supprimer_une_tache():
    c = client()
    t = c.post("/api/taches", json={"titre": "Tâche à supprimer"}).get_json()
    maj = c.patch(f"/api/taches/{t['id']}").get_json()
    assert maj["terminee"] is True
    assert c.delete(f"/api/taches/{t['id']}").status_code == 204
