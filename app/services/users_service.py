from __future__ import annotations

from app.factories.users_factory_protocol import IUsersFactory
from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate


class UsersService:
    """
    Service applicatif : orchestre la logique Users.

    - charge les users via la factory (source JSON pour ce TP)
    - expose list/get/create
    - persistance en mémoire (volontairement simple)
    """

    def __init__(self, factory: IUsersFactory, users_json_path: str) -> None:
        self._factory = factory
        self._users: list[UserModel] = factory.create_users(users_json_path)

    def list_users(self) -> list[UserModel]:
        return list(self._users)

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        for u in self._users:
            if u.id == user_id:
                return u
        return None

    def create_user(self, payload: UserModelCreate) -> UserModel:
        next_id = max((u.id for u in self._users), default=0) + 1

        created = UserModel(
            id=next_id,
            login=payload.login,
            age=payload.age,
        )
        self._users.append(created)
        return created
