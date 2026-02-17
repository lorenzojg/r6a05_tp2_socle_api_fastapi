from __future__ import annotations

from typing import Protocol
from app.models.user_model import UserModel


class IUsersFactory(Protocol):
    """Contrat : charge un fichier JSON et retourne une liste de UserModel."""

    def create_users(self, json_path: str) -> list[UserModel]:
        ...
