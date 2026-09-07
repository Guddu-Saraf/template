def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "test@example.com"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "test@example.com"
    assert "id" in data


def test_get_users(client):
    response = client.get("/users/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_duplicate_email(client):
    client.post(
        "/users/",
        json={"email": "duplicate@example.com"},
    )

    response = client.post(
        "/users/",
        json={"email": "duplicate@example.com"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_invalid_user_data(client):
    response = client.post(
        "/users/",
        json={},
    )

    assert response.status_code == 422

    