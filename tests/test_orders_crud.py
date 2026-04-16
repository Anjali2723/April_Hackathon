def create_admin_and_user(client):
    admin = client.post("/users/", json={"name": "Admin", "email": "admin@test.com", "role": "admin"}).json()
    user = client.post("/users/", json={"name": "User", "email": "user@test.com", "role": "user"}).json()
    return admin["id"], user["id"]

def test_create_order(client):
    admin_id, user_id = create_admin_and_user(client)
    r = client.post("/orders/", headers={"X-User-Id": str(user_id)}, json={"total_amount": 100, "status": "created"})
    assert r.status_code == 200
    assert r.json()["user_id"] == user_id

def test_read_order(client):
    admin_id, user_id = create_admin_and_user(client)
    created = client.post("/orders/", headers={"X-User-Id": str(user_id)}, json={"total_amount": 100}).json()
    oid = created["id"]
    r = client.get(f"/orders/{oid}", headers={"X-User-Id": str(user_id)})
    assert r.status_code == 200
    assert r.json()["id"] == oid

def test_update_order(client):
    admin_id, user_id = create_admin_and_user(client)
    created = client.post("/orders/", headers={"X-User-Id": str(user_id)}, json={"total_amount": 100}).json()
    oid = created["id"]
    r = client.put(f"/orders/{oid}", headers={"X-User-Id": str(user_id)}, json={"status": "paid"})
    assert r.status_code == 200
    assert r.json()["status"] == "paid"

def test_delete_order(client):
    admin_id, user_id = create_admin_and_user(client)
    created = client.post("/orders/", headers={"X-User-Id": str(user_id)}, json={"total_amount": 100}).json()
    oid = created["id"]
    r = client.delete(f"/orders/{oid}", headers={"X-User-Id": str(user_id)})
    assert r.status_code == 200
