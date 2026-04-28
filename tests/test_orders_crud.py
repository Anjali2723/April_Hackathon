def create_admin_and_user(client):
    admin = client.post("/users/", json={
        "name": "Admin",
        "email": "admin@test.com",
        "password": "adminpass",
        "role": "admin",
    })
    assert admin.status_code == 200
    admin_id = admin.json()["id"]

    user = client.post("/users/", json={
        "name": "User",
        "email": "user@test.com",
        "password": "userpass",
        "role": "user",
    })
    assert user.status_code == 200
    user_id = user.json()["id"]

    return admin_id, user_id


def test_create_order(client):
    admin_id, user_id = create_admin_and_user(client)

    r = client.post("/orders/", json={
        "total_amount": 100,
        "status": "created",
    }, headers={"X-User-Id": str(user_id)})

    assert r.status_code == 200
    assert "id" in r.json()


def test_read_order(client):
    admin_id, user_id = create_admin_and_user(client)

    create = client.post("/orders/", json={
        "total_amount": 100,
        "status": "created",
    }, headers={"X-User-Id": str(user_id)})
    assert create.status_code == 200
    oid = create.json()["id"]

    r = client.get(f"/orders/{oid}", headers={"X-User-Id": str(user_id)})
    assert r.status_code == 200
    assert r.json()["id"] == oid


def test_update_order(client):
    admin_id, user_id = create_admin_and_user(client)

    create = client.post("/orders/", json={
        "total_amount": 100,
        "status": "created",
    }, headers={"X-User-Id": str(user_id)})
    assert create.status_code == 200
    oid = create.json()["id"]

    r = client.put(f"/orders/{oid}", json={
        "status": "paid",
    }, headers={"X-User-Id": str(user_id)})

    assert r.status_code == 200
    assert r.json()["status"] == "paid"


def test_delete_order(client):
    admin_id, user_id = create_admin_and_user(client)

    create = client.post("/orders/", json={
        "total_amount": 100,
        "status": "created",
    }, headers={"X-User-Id": str(user_id)})
    assert create.status_code == 200
    oid = create.json()["id"]

    r = client.delete(f"/orders/{oid}", headers={"X-User-Id": str(user_id)})
    assert r.status_code == 200
