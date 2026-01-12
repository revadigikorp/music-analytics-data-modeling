import pytest
from sqlalchemy import create_engine, text
from src.config import DATABASE_URL

@pytest.fixture
def engine():
    return create_engine(DATABASE_URL)

def test_tables_not_empty(engine):
    with engine.connect() as conn:
        for table in ['users', 'songs', 'artists', 'time', 'songplays']:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            assert result >= 0