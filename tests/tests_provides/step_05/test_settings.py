"""
Tests unitaires de la configuration.

Objectif :
- vérifier le comportement par défaut,
- vérifier la surcharge via variable d'environnement,
- garantir l'isolation des tests.
"""

import pytest
from app.core.settings import Settings


def test_should_use_default_users_json_path_when_env_not_set(monkeypatch):
    """
    Vérifie que la valeur par défaut est utilisée si USERS_JSON_PATH n'est pas définie.
    """
    # Arrange
    monkeypatch.delenv("USERS_JSON_PATH", raising=False)

    # Act
    settings = Settings()

    # Assert (1 assertion métier)
    assert settings.users_json_path == "data/users.json"


def test_should_use_env_value_when_defined(monkeypatch):
    """
    Vérifie que la variable d'environnement surcharge la valeur par défaut.
    """
    # Arrange
    monkeypatch.setenv("USERS_JSON_PATH", "custom/path.json")

    # Act
    settings = Settings()

    # Assert (1 assertion métier)
    assert settings.users_json_path == "custom/path.json"