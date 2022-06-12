import pytest

from src.store.models.users import User
from src.core.config import settings
from src.core.jwt import create_access_token
from tests.conf_test_db import override_get_db


@pytest.fixture(autouse=True)
def base_url():
    return f"http://test/{settings.API_VERSION_STR}"


@pytest.fixture(autouse=True)
def user_data():
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test_user@gmail.com",
        "password": "test_user123",
    }

    return data


@pytest.fixture(autouse=True)
def headers(user_data):
    user_access_token = create_access_token({"sub": user_data["email"]})
    headers={"Authorization": f"Bearer {user_access_token}"}

    return headers


@pytest.fixture(autouse=True)
def create_testing_user(tmpdir, user_data):
    from tests.conf_test_db import override_get_db

    database = next(override_get_db())
    new_user = User(first_name=user_data["first_name"], last_name=user_data["last_name"], email=user_data["email"], password=user_data["password"])
    database.add(new_user)
    database.commit()

    yield

    database.query(User).filter(User.email == user_data["email"]).delete()
    database.commit()



def get_user_by_mail(email):
    database = next(override_get_db())
    return database.query(User).filter(User.email == email).first()

