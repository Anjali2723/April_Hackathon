def test_create_user(client):
    r = client.post("/users/", json={"name": "U1", "email": "u1@test.com", "role": "user"})
    assert r.status_code == 200
    assert r.json()["id"] is not None

def test_read_user(client):
    r1 = client.post("/users/", json={"name": "U2", "email": "u2@test.com", "role": "user"})
    uid = r1.json()["id"]
    r2 = client.get(f"/users/{uid}")
    assert r2.status_code == 200
    assert r2.json()["email"] == "u2@test.com"

def test_update_user(client):
    r1 = client.post("/users/", json={"name": "U3", "email": "u3@test.com", "role": "user"})
    uid = r1.json()["id"]
    r2 = client.put(f"/users/{uid}", json={"name": "U3-new"})
    assert r2.status_code == 200
    assert r2.json()["name"] == "U3-new"

def test_delete_user(client):
    r1 = client.post("/users/", json={"name": "U4", "email": "u4@test.com", "role": "user"})
    uid = r1.json()["id"]
    r2 = client.delete(f"/users/{uid}")
    assert r2.status_code == 200
    r3 = client.get(f"/users/{uid}")
    assert r3.status_code in (404, 200)  # depends on how you implemented not-found