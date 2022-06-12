import pytest
from httpx import AsyncClient

from tests.conf_test_db import app


@pytest.mark.asyncio
async def test_auth(base_url):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@gmail.com",
            "password": "test_user1232",
        }

        auth_data = {
            "username": data["email"],
            "password": data["password"],
            }

        new_user = await ac.post(f"/users/", json=data)

        r = await ac.post("/auth/login", data=auth_data)

    assert r.status_code == 200
    assert "access_token" in r.json()
    assert r.json()["token_type"] == "bearer"

