import pytest
from sqlalchemy import create_engine , select
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy import text

from infrastructure.persistence.orm.models  import metadata


@pytest.fixture
def in_memory_db():
    engine=create_engine('sqlite://',echo=True)
    metadata.create_all(engine)
    with engine.connect() as conn:
        result = conn.execute(text('pragma foreign_keys=on'))
    return engine


@pytest.fixture
def session(in_memory_db):
    yield sessionmaker(bind=in_memory_db)()


    