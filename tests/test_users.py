def test_update_user(client):
    # create user first
    create = client.post(
        "/users/",
        json={"name": "Old", "email": "old@test.com"}
    )
    user_id = create.json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={"name": "Updated"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated"