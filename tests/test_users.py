import pytest
from httpx import AsyncClient
from src.main import app

USERNAME = "chaplygin"

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/{USERNAME}/users/", json={"name": "TestUser"})
        assert response.status_code == 200
        assert response.json()["name"] == "TestUser"

@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/{USERNAME}/users/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_user_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/{USERNAME}/users/99999")
        assert response.status_code == 404
