"""
Rôle de ce fichier de test :

Valider le comportement de UsersFactory indépendamment du reste de l'application.

Objectifs pédagogiques :
- vérifier que la factory transforme correctement un JSON en objets UserModel,
- garantir que les erreurs sont explicites et contrôlées,
- isoler la couche "transformation JSON → objets métier",
- ne dépendre ni de FastAPI, ni de Settings, ni de la base de données.

Ces tests doivent passer AVANT d’introduire le repository ou le service.
"""

import json
import pytest

from app.factories.users_factory import UsersFactory


def test_should_create_users_given_valid_json(tmp_path):
    # Arrange
    payload = {
        "users": [
            {"id": 1, "login": "alice", "age": 20},
            {"id": 2, "login": "bob", "age": 22},
        ]
    }
    p = tmp_path / "users.json"
    p.write_text(json.dumps(payload), encoding="utf-8")

    factory = UsersFactory()

    # Act
    users = factory.create_users(str(p))

    # Assert (1 assertion métier)
    assert len(users) == 2


def test_should_raise_value_error_given_missing_users_key(tmp_path):
    # Arrange
    payload = {"not_users": []}
    p = tmp_path / "users.json"
    p.write_text(json.dumps(payload), encoding="utf-8")

    factory = UsersFactory()

    # Act / Assert (1 assertion métier)
    with pytest.raises(ValueError, match="No users found"):
        factory.create_users(str(p))


def test_should_raise_file_not_found_error_given_missing_file(tmp_path):
    # Arrange
    missing = tmp_path / "missing.json"
    factory = UsersFactory()

    # Act / Assert (1 assertion métier)
    with pytest.raises(FileNotFoundError):
        factory.create_users(str(missing))


def test_should_raise_value_error_given_users_is_not_a_list(tmp_path):
    # Arrange
    payload = {"users": {"id": 1, "login": "alice", "age": 20}}  # pas une liste
    p = tmp_path / "users.json"
    p.write_text(json.dumps(payload), encoding="utf-8")

    factory = UsersFactory()

    # Act / Assert (1 assertion métier)
    with pytest.raises(ValueError):
        factory.create_users(str(p))