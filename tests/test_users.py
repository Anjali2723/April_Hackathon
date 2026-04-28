def test_update_user(client):
    # create admin
    admin = client.post("/users/", json={
        "name": "Admin",
        "email": "admin@test.com",
        "password": "adminpass",
        "role": "admin",
    })
    assert admin.status_code == 200
    admin_id = admin.json()["id"]

    # create normal user
    create = client.post("/users/", json={
        "name": "Old",
        "email": "old@test.com",
        "password": "password123",
        "role": "user",
    })
    assert create.status_code == 200
    user_id = create.json()["id"]

    # update requires admin header
    update = client.put(
        f"/users/{user_id}",
        json={"name": "New"},
        headers={"X-User-Id": str(admin_id)},
    )
    assert update.status_code == 200
    assert update.json()["name"] == "New"
