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
        
    def list_users(self) -> list[UserModel]:
        return list(self._repository.list_users())

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        for u in self._repository.list_users():
            if u.id == user_id:
                return u
        return None

    def create_user(self, payload: UserModelCreate) -> UserModel:
        next_id = max((u.id for u in self._repository.list_users()), default=0) + 1

        created = UserModel(
            id=next_id,
            login=payload.login,
            age=payload.age,
        )

        self._repository.create_user(UserModelCreate(login=created.login, age=created.age))

        return created
