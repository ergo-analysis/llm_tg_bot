import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_user(client: AsyncClient):
    resp = await client.post(
        "/auth/register",
        json={"email": "newuser@email.com", "password": "securepass"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "newuser@email.com"
    assert "id" in data
    assert data["role"] == "user"
    assert "created_at" in data


async def test_register_duplicate_user(client: AsyncClient, test_user):
    resp = await client.post(
        "/auth/register",
        json={"email": test_user["email"], "password": "anotherpass"}
    )
    assert resp.status_code == 409
    assert "already exists" in resp.json()["detail"]


async def test_login_success(client: AsyncClient, test_user):
    resp = await client.post(
        "/auth/login",
        data={"username": test_user["email"], "password": "testpass123"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client: AsyncClient, test_user):
    resp = await client.post(
        "/auth/login",
        data={"username": test_user["email"], "password": "wrongpass"}
    )
    assert resp.status_code == 401


async def test_get_me_with_valid_token(client: AsyncClient, test_user):

    login_resp = await client.post(
        "/auth/login",
        data={"username": test_user["email"], "password": "testpass123"}
    )
    token = login_resp.json()["access_token"]

    resp = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == test_user["email"]
    assert data["role"] == "user"
    assert "created_at" in data


async def test_get_me_without_token(client: AsyncClient):
    resp = await client.get("/auth/me")
    assert resp.status_code == 401


async def test_get_me_with_invalid_token(client: AsyncClient):
    resp = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert resp.status_code == 401
    