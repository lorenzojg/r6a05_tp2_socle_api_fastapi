from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy.orm import sessionmaker

from app.core.settings import get_settings
from app.db.engine import get_engine
from app.repositories.users_repository_sql import SqlAlchemyUsersRepository
from app.models.user_model_create import UserModelCreate


# -------------------------
# Helpers tests
# -------------------------

def _write_users_json(path: Path, n: int) -> None:
    """
    Crée un JSON minimal pour le test :
    { "users": [ {"login": "...", "age": ...}, ... ] }
    """
    users = [{"login": f"user{i}", "age": 18 + (i % 10)} for i in range(1, n + 1)]
    payload = {"users": users}
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _build_session_local():
    """
    Construit SessionLocal à partir de l'engine courant (lié aux env).
    """
    engine = get_engine()
    return sessionmaker(bind=engine)


# -------------------------
# Tests (AAA)
# -------------------------

def test_should_list_users_from_sqlite_given_seeded_db(tmp_path: Path, monkeypatch):
    """
    Rôle du test :
    - vérifier que list_users() lit bien les données en base
    - sans dépendre de FastAPI
    - avec une DB SQLite temporaire
    """
    # Arrange
    db_file = tmp_path / "test.db"
    json_file = tmp_path / "users.json"
    _write_users_json(json_file, n=3)

    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{db_file}")
    monkeypatch.setenv("USERS_JSON_PATH", str(json_file))
    get_settings.cache_clear()

    # Seed via le script (tables + insert)
    from scripts.seed_users import main as seed_main
    inserted = seed_main()
    assert inserted == 3  # assertion "technique" OK ici (optionnelle)

    SessionLocal = _build_session_local()

    # Act
    with SessionLocal() as db:
        repo = SqlAlchemyUsersRepository(db)
        users = repo.list_users()

    # Assert (1 assertion métier)
    assert len(users) == 3


def test_should_return_none_given_unknown_user_id(tmp_path: Path, monkeypatch):
    """
    Rôle du test :
    - vérifier get_user_by_id() retourne None si l'id n'existe pas
    """
    # Arrange
    db_file = tmp_path / "test.db"
    json_file = tmp_path / "users.json"
    _write_users_json(json_file, n=2)

    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{db_file}")
    monkeypatch.setenv("USERS_JSON_PATH", str(json_file))
    get_settings.cache_clear()

    from scripts.seed_users import main as seed_main
    seed_main()

    SessionLocal = _build_session_local()

    # Act
    with SessionLocal() as db:
        repo = SqlAlchemyUsersRepository(db)
        user = repo.get_user_by_id(9999)

    # Assert (1 assertion métier)
    assert user is None


def test_should_create_user_and_return_generated_id(tmp_path: Path, monkeypatch):
    """
    Rôle du test :
    - vérifier create_user() insère en base
    - et renvoie un id généré automatiquement
    """
    # Arrange
    db_file = tmp_path / "test.db"

    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{db_file}")
    # USERS_JSON_PATH n'est pas nécessaire ici (on ne seed pas)
    get_settings.cache_clear()

    # Création des tables (sans seed)
    from scripts.seed_users import create_tables
    create_tables()

    payload = UserModelCreate(login="alice", age=25)

    SessionLocal = _build_session_local()

    # Act
    with SessionLocal() as db:
        repo = SqlAlchemyUsersRepository(db)
        created = repo.create_user(payload)

    # Assert (1 assertion métier)
    assert created.id >= 1