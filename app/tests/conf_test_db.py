from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import config
from src.store.db import get_store, Base
# from src.store.base_class import Base
from src.main import app


SQLALCHEMY_DATABASE_URL = config.SQLALCHEMY_TEST_DATABASE_URL
print(SQLALCHEMY_DATABASE_URL)
print(Base)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator:
    try:
        db = TestSessionLocal()
        db.expire_on_commit = False
        yield db

    finally:
        db.close()

app.dependency_overrides[get_store] = override_get_db

