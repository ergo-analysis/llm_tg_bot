import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

CREDENTIALS = {
            "email": "surname@email.com",
            "password": "pass1234"
        }


class TestAuthFullFlow:
    async def test_register_login_me(self, client: AsyncClient):

        user_email = "surname@email.com"
        password = "pass1234"

        reg_data = {"email": user_email, "password": password}
        resp = await client.post("/auth/register", json=reg_data)
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == reg_data["email"]
        assert "id" in data

        login_data = {"username": user_email, "password": password}
        resp = await client.post("/auth/login", data=login_data)
        assert resp.status_code == 200
        token = resp.json()["access_token"]

        resp = await client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        assert resp.status_code == 200
        me = resp.json()
        assert me["email"] == login_data["username"]


    async def test_duplicate_registration_returns_409(self, client: AsyncClient):

        dub_credentials = {
            "email": "dup@email.com", "password": "pass123"
        }

        await client.post("/auth/register", json=dub_credentials)
        resp = await client.post("/auth/register", json=dub_credentials)
        assert resp.status_code == 409

    async def test_login_invalid_password_returns_401(self, client: AsyncClient):

        user_email = "surname@email.com"
        correct_password = "correct_password"
        wrong_password = "wrong_password"

        reg_data = {"email": user_email, "password": correct_password}
        await client.post("/auth/register", json=reg_data)

        login_data = {"username": user_email, "password": wrong_password}
        resp = await client.post("/auth/login", data=login_data)
        assert resp.status_code == 401

    async def test_me_without_token_returns_401(self, client: AsyncClient):
        resp = await client.get("/auth/me")
        assert resp.status_code == 401

    async def test_me_with_invalid_token_returns_401(self, client: AsyncClient):
        resp = await client.get("/auth/me", headers={
            "Authorization": "Bearer invalidtoken"
        })
        assert resp.status_code == 401
