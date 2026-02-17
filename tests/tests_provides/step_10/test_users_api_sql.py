from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.db.base import Base
from app.api.dependencies import get_users_service
from app.db.session import get_db
from app.repositories.users_repository_sql import SqlAlchemyUsersRepository
from app.services.users_service import UsersService
from app.models_orm.user_table import UserTable


def test_should_list_users_with_sqlite_test_db(tmp_path):
    # Arrange : DB temporaire
    db_file = tmp_path / "test.db"
    engine = create_engine(f"sqlite+pysqlite:///{db_file}", future=True)

    Base.metadata.create_all(engine)

    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    # Seed minimal
    with TestingSessionLocal() as db:
        db.add_all([
            UserTable(id=1, login="alice", age=20),
            UserTable(id=2, login="bob", age=21),
        ])
        db.commit()

    # Override get_db
    def _override_get_db():
        db: Session = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Override get_users_service -> service réel branché sur DB test
    def _override_get_users_service():
        # on récupère une session via l’override get_db (FastAPI gère yield)
        # Ici version simple : on ouvre une session directement pour construire le service.
        db: Session = TestingSessionLocal()
        repo = SqlAlchemyUsersRepository(db)
        return UsersService(repo)

    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_users_service] = _override_get_users_service

    client = TestClient(app)

    # Act
    r = client.get("/users")

    # Assert
    assert r.status_code == 200
    assert len(r.json()) == 2
    assert r.json()[0]["login"] == "alice"

    # Cleanup
    app.dependency_overrides.clear()