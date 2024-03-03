import pytest
from src.db.engine import engine
from src.db.models import Base


@pytest.fixture(name="db")
def create_db():
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
