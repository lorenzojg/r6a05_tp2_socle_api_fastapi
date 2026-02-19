from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import select, func
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import get_settings
from app.db.base import Base
from app.db.engine import get_engine
from app.models_orm.user_table import UserTable


def create_tables() -> None:
    """
    Crée les tables ORM si elles n'existent pas.

    Important :
    - importer UserTable avant create_all (sinon la table n'est pas connue du metadata)
    """
    engine = get_engine()
    Base.metadata.create_all(engine)


def _is_table_empty(db: Session) -> bool:
    """
    Indique si la table users est vide.
    """
    count = db.scalar(select(func.count()).select_from(UserTable))
    return count == 0


def seed_users(db: Session, json_path: str) -> int:
    """
    Insère les utilisateurs depuis un fichier JSON si la table est vide.

    Contraintes :
    - si la clé 'users' est absente ou vide -> ValueError("No users found")
    - idempotent : si la table n'est pas vide -> 0 insertion

    Returns:
        int: nombre d'insertions effectuées.
    """
    if not _is_table_empty(db):
        return 0

    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    users = data.get("users")
    if not users:
        raise ValueError("No users found")

    for u in users:
        db.add(UserTable(login=u["login"], age=u["age"]))

    db.commit()
    return len(users)


def main() -> int:
    """
    Point d'entrée du script.

    - lit Settings (DATABASE_URL + USERS_JSON_PATH)
    - crée les tables
    - ouvre une session
    - seed
    """
    settings = get_settings()

    create_tables()

    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as db:
        inserted = seed_users(db, settings.users_json_path)
        print(f"Inserted: {inserted}")
        return inserted


if __name__ == "__main__":
    raise SystemExit(main())