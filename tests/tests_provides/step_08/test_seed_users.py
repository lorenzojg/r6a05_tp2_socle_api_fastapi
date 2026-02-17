from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker

from app.core.settings import get_settings
from app.db.engine import get_engine
from app.models_orm.user_table import UserTable


def _write_users_json(path: Path, n: int) -> None:
    users = [{"login": f"user{i}", "age": 18 + (i % 10)} for i in range(1, n + 1)]
    path.write_text(json.dumps({"users": users}, ensure_ascii=False), encoding="utf-8")


def test_should_create_tables_and_seed_by_calling_script_main(tmp_path: Path, monkeypatch):
    # Arrange
    db_file = tmp_path / "test.db"
    json_file = tmp_path / "users.json"
    _write_users_json(json_file, n=5)

    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{db_file}")
    monkeypatch.setenv("USERS_JSON_PATH", str(json_file))

    # IMPORTANT : Settings est caché -> on vide le cache
    get_settings.cache_clear()

    # Act : on appelle le script (son main)
    from scripts.seed_users import main
    inserted = main()

    # Assert : on vérifie N insertions + N lignes en base
    assert inserted == 5

    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as db:
        count = db.scalar(select(func.count()).select_from(UserTable))
    assert count == 5


def test_should_be_idempotent_when_called_twice(tmp_path: Path, monkeypatch):
    # Arrange
    db_file = tmp_path / "test.db"
    json_file = tmp_path / "users.json"
    _write_users_json(json_file, n=3)

    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{db_file}")
    monkeypatch.setenv("USERS_JSON_PATH", str(json_file))
    get_settings.cache_clear()

    from scripts.seed_users import main

    # Act
    inserted_1 = main()
    get_settings.cache_clear()  # (relecture env ok, mais optionnel ici)
    inserted_2 = main()

    # Assert
    assert inserted_1 == 3
    assert inserted_2 == 0