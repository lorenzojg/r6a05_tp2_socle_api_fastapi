"""
Tests infra DB — Connexion.

Objectif :
- vérifier que l'Engine peut ouvrir une connexion
- vérifier qu'une requête SQL minimale fonctionne
"""

from sqlalchemy import text

from app.db.engine import get_engine


def test_should_connect_to_db_and_execute_select_1():
    # Arrange
    engine = get_engine()

    # Act
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()

    # Assert (1 assertion métier)
    assert result == 1