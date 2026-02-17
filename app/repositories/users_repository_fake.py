from .protocols.IUsersRepository import IUsersRepository
from app.models.user_model import UserModel
from app.factories.users_factory import UsersFactory
from app.services.users_service import UsersService


class FakeUsersRepository(IUsersRepository):
    """Implémentation de IUsersRepository pour les tests."""
    def __init__(self, factory: UsersFactory, json_path: str) -> None:
        self._factory = factory
        self._json_path = json_path
        self._service = UsersService(repository=self)

    def list_users(self) -> list[UserModel]:
        return self._service.list_users()
    
    def get_user_by_id(self, user_id: int):
        return self._service.get_user_by_id(user_id)

    def create_user(self, user):
        return self._service.create_user(user)