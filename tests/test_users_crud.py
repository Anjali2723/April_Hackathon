def test_create_user(client):
    r = client.post("/users/", json={
        "name": "U1",
        "email": "u1@test.com",
        "password": "password123",
        "role": "user",
    })
    assert r.status_code == 200
    assert "id" in r.json()


def test_read_user(client):
    r1 = client.post("/users/", json={
        "name": "U2",
        "email": "u2@test.com",
        "password": "password123",
        "role": "user",
    })
    assert r1.status_code == 200
    uid = r1.json()["id"]

    r2 = client.get(f"/users/{uid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == uid


def test_update_user(client):
    # create admin (needed for RBAC)
    admin = client.post("/users/", json={
        "name": "Admin",
        "email": "admin@test.com",
        "password": "adminpass",
        "role": "admin",
    })
    assert admin.status_code == 200
    admin_id = admin.json()["id"]

    # create user to update
    r1 = client.post("/users/", json={
        "name": "U3",
        "email": "u3@test.com",
        "password": "password123",
        "role": "user",
    })
    assert r1.status_code == 200
    uid = r1.json()["id"]

    # update requires admin header
    r2 = client.put(
        f"/users/{uid}",
        json={"name": "U3-updated"},
        headers={"X-User-Id": str(admin_id)},
    )
    assert r2.status_code == 200
    assert r2.json()["name"] == "U3-updated"


def test_delete_user(client):
    # create admin (needed for RBAC)
    admin = client.post("/users/", json={
        "name": "Admin2",
        "email": "admin2@test.com",
        "password": "adminpass",
        "role": "admin",
    })
    assert admin.status_code == 200
    admin_id = admin.json()["id"]

    # create user to delete
    r1 = client.post("/users/", json={
        "name": "U4",
        "email": "u4@test.com",
        "password": "password123",
        "role": "user",
    })
    assert r1.status_code == 200
    uid = r1.json()["id"]

    # delete requires admin header
    r2 = client.delete(
        f"/users/{uid}",
        headers={"X-User-Id": str(admin_id)},
    )
    assert r2.status_code == 200
