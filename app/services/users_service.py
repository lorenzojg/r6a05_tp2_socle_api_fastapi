from __future__ import annotations

from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate
from app.repositories.protocols.IUsersRepository import IUsersRepository

class UsersService:
    """
    Service applicatif : orchestre la logique Users.

    - charge les users via la factory (source JSON pour ce TP)
    - expose list/get/create
    - persistance en mémoire (volontairement simple)
    """

    def __init__(self, repository : IUsersRepository) -> None:
        self._repository = repository
        self._users: list[UserModel] = self._repository.list_users()

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
