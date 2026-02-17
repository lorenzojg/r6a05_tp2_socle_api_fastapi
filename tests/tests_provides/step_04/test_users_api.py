"""
Tests d'intégration de l'API FastAPI.

Objectif :
- vérifier les codes HTTP
- vérifier la validation automatique
- tester Router + Service + FakeRepo ensemble (profil fake)
"""


def test_should_list_users_given_existing_users(client):
    # Arrange
    # (la fixture client prépare 2 utilisateurs)

    # Act
    response = client.get("/users")

    # Assert (1 assertion métier)
    assert len(response.json()) == 2


def test_should_get_user_by_id_given_existing_id(client):
    # Arrange
    user_id = 1

    # Act
    response = client.get(f"/users/{user_id}")

    # Assert (1 assertion métier)
    assert response.json()["login"] == "alice"


def test_should_return_404_given_unknown_user_id(client):
    # Arrange
    user_id = 99999

    # Act
    response = client.get(f"/users/{user_id}")

    # Assert (1 assertion métier)
    assert response.status_code == 404


def test_should_create_user_given_valid_payload(client):
    # Arrange
    payload = {"login": "integration_test", "age": 30}

    # Act
    response = client.post("/users", json=payload)

    # Assert (1 assertion métier)
    assert response.json()["login"] == "integration_test"


def test_should_return_422_given_invalid_payload(client):
    # Arrange
    payload = {"login": "missing_age"}

    # Act
    response = client.post("/users", json=payload)

    # Assert (1 assertion métier)
    assert response.status_code == 422
