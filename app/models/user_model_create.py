from pydantic import BaseModel, Field


class UserModelCreate(BaseModel):
    """Modèle d'entrée (création) : le client ne fournit pas l'id."""

    login: str = Field(min_length=3)
    age: int = Field(gt=0)
