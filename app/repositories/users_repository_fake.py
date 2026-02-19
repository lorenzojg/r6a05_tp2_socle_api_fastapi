from .protocols.IUsersRepository import IUsersRepository
from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate
from app.factories.users_factory import UsersFactory


class FakeUsersRepository(IUsersRepository):
    """Implémentation en mémoire de IUsersRepository (chargée depuis un JSON)."""

    def __init__(self, factory: UsersFactory, json_path: str) -> None:
        self._users: list[UserModel] = factory.create_users(json_path)

    def list_users(self) -> list[UserModel]:
        return list(self._users)

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        for u in self._users:
            if u.id == user_id:
                return u
        return None

    def create_user(self, user: UserModelCreate) -> UserModel:
        next_id = max((u.id for u in self._users), default=0) + 1
        new_user = UserModel(id=next_id, login=user.login, age=user.age)
        self._users.append(new_user)
        return new_user