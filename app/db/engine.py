from __future__ import annotations

from sqlalchemy import create_engine
from app.core.settings import get_settings


def get_engine():
    """
    Construit l'engine SQLAlchemy à partir de Settings.database_url.
    """
    settings = get_settings()
    return create_engine(settings.database_url, echo=False)