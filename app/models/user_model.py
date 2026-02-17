from pydantic import BaseModel


class UserModel(BaseModel):
    """Modèle persisté / lecture : l'utilisateur a un id."""

    id: int
    login: str
    age: int
