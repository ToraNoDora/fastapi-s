import pytest
from httpx import AsyncClient
from faker import Faker

from tests.conf_test_db import app
from tests.conftest import get_user_by_mail
from src.redis.cache import RedisCache


@pytest.mark.asyncio
async def test_registration(base_url):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        status_code, new_user, user_data = await _create_new_user(ac)

    assert status_code == 201
    assert "password" in new_user
    assert "id" in new_user

    assert new_user["first_name"] == user_data["first_name"]
    assert new_user["last_name"] == user_data["last_name"]
    assert new_user["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_get_user(base_url, headers):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        _, new_user, _ = await _create_new_user(ac)
        r = await ac.get(f"/users/{new_user['id']}", headers=headers)

        async with RedisCache() as cache:
            print("TEST delete user")
            await cache.delete(f"user {new_user['id']}")
            # await cache.delete("all users")

    assert r.status_code == 200

    assert r.json()["first_name"] == new_user["first_name"]
    assert r.json()["last_name"] == new_user["last_name"]
    assert r.json()["email"] == new_user["email"]


@pytest.mark.asyncio
async def test_update_user(base_url, headers, user_data):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        # _, new_user, user_data = await _create_new_user(ac)
        user = get_user_by_mail(user_data["email"]).to_dict()

        data = {
            "first_name": "New first",
            "last_name": "New last",
            "email": "test_user@gmail.com",
            # "password": "test_user123",
        }

        r = await ac.put(f"/users/{user['id']}", json=data, headers=headers)
        print(r.json())

    assert r.status_code == 201

    assert r.json()["first_name"] != user["first_name"]
    assert r.json()["last_name"] != user["last_name"]
    # assert r.json()["email"] != user["email"]


@pytest.mark.asyncio
async def test_all_users(base_url, user_data, headers):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        async with RedisCache() as cache:
            print("TEST delete userSSSSSSSSSSSS")
            await cache.delete("all users")

        all_users = await ac.get("/users/", headers=headers)

    assert all_users.status_code == 200

    assert len(all_users.json()) > 1
    # assert all_users.json()[-1]["first_name"] == user_data["first_name"]
    # assert all_users.json()[-1]["last_name"] == user_data["last_name"]
    # assert all_users.json()[-1]["email"] == user_data["email"]


async def _create_new_user(ac: AsyncClient):
    faker = Faker()

    user_data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "password": faker.password(),
    }

    new_user = await ac.post("/users/", json=user_data)

    return new_user.status_code, new_user.json(), user_data