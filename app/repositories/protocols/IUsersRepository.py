from __future__ import annotations

from typing import Protocol

from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate

class IUsersRepository(Protocol):
    """
    Contrat d'accès aux données utilisateur.

    Objectif :
    - fournir une API stable au service,
    - masquer la source réelle (JSON, SQLite, etc.),
    - permettre de remplacer l'infrascture sans modifier le service ni les routes.
    """

    def list_users(self) -> list[UserModel]:
        """Retourne la liste des utilisateurs."""
        ...

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        """Retourne l'utilisateur d'identifiant user_id, ou None si introuvable."""
        ...

    def create_user(self, user: UserModelCreate) -> UserModel:
        """Crée un utilisateur et retourne l'utilisateur créé."""
        ...