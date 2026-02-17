from __future__ import annotations

"""
Tests de composition (Partie 2)

Objectif :
- vérifier la bascule APP_PROFILE=fake / APP_PROFILE=sql
- sans lancer FastAPI
- en testant uniquement la logique de construction du service (DI)

Principe :
- on monkeypatch `app.api.dependencies.get_settings` pour contrôler le profil
- on appelle `get_users_service(db=...)` directement (sans Depends)
- on vérifie que la bonne implémentation de repository est instanciée
"""

from dataclasses import dataclass

from sqlalchemy.orm import Session

import app.api.dependencies as deps


class _FakeSession(Session):
    """
    Session factice.

    Remarque :
    - on ne fait aucune requête SQL
    - elle sert uniquement à fournir une instance typée `Session`
      quand le profil est "sql"
    """

    pass


@dataclass(frozen=True)
class _SettingsFake:
    """Settings minimal pour les tests (profil fake)."""

    app_profile: str = "fake"
    users_json_path: str = "data/users.json"


@dataclass(frozen=True)
class _SettingsSql:
    """Settings minimal pour les tests (profil sql)."""

    app_profile: str = "sql"
    users_json_path: str = "data/users.json"


def test_should_build_fake_repository_via_get_users_service_given_profile_fake(monkeypatch):
    """
    Rôle du test :
    - vérifier que `get_users_service(...)` construit le service avec FakeUsersRepository
      lorsque Settings.app_profile == "fake".
    """

    # Arrange
    called = {"fake": 0, "sql": 0}

    class _FakeRepoSpy:
        """Spy qui remplace FakeUsersRepository pour vérifier l'instanciation."""

        def __init__(self, factory, json_path: str) -> None:  # noqa: ANN001
            called["fake"] += 1

    class _SqlRepoSpy:
        """Spy qui remplace SqlAlchemyUsersRepository pour vérifier l'instanciation."""

        def __init__(self, db: Session) -> None:
            called["sql"] += 1

    monkeypatch.setattr(deps, "get_settings", lambda: _SettingsFake())
    monkeypatch.setattr(deps, "FakeUsersRepository", _FakeRepoSpy)
    monkeypatch.setattr(deps, "SqlAlchemyUsersRepository", _SqlRepoSpy)

    # Act
    _ = deps.get_users_service(db=_FakeSession())

    # Assert (1 assertion métier)
    assert called["fake"] == 1


def test_should_build_sql_repository_via_get_users_service_given_profile_sql(monkeypatch):
    """
    Rôle du test :
    - vérifier que `get_users_service(...)` construit le service avec SqlAlchemyUsersRepository
      lorsque Settings.app_profile == "sql".
    """

    # Arrange
    called = {"fake": 0, "sql": 0}

    class _FakeRepoSpy:
        def __init__(self, factory, json_path: str) -> None:  # noqa: ANN001
            called["fake"] += 1

    class _SqlRepoSpy:
        def __init__(self, db: Session) -> None:
            called["sql"] += 1

    monkeypatch.setattr(deps, "get_settings", lambda: _SettingsSql())
    monkeypatch.setattr(deps, "FakeUsersRepository", _FakeRepoSpy)
    monkeypatch.setattr(deps, "SqlAlchemyUsersRepository", _SqlRepoSpy)

    # Act
    _ = deps.get_users_service(db=_FakeSession())

    # Assert (1 assertion métier)
    assert called["sql"] == 1
