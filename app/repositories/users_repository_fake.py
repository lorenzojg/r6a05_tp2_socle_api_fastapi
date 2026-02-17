from .protocols.IUsersRepository import IUsersRepository
from app.models.user_model import UserModel
from app.factories.users_factory import UsersFactory
from app.services.users_service import UsersService
from app.api.routers.users_router import get_users_service


class FakeUsersRepository(IUsersRepository):
    """Implémentation de IUsersRepository pour les tests."""
    def __init__(self, factory: UsersFactory, json_path: str) -> None:
        self._factory = factory
        self._json_path = json_path

    def list_users(self) -> list[UserModel]:
        return get_users_service().list_users()
    
    def get_user_by_id(self, user_id: int):
        return get_users_service().get_user_by_id(user_id)

    def create_user(self, user):
        return get_users_service().create_user(user)