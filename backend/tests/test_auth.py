import pytest

@pytest.mark.asyncio
async def test_register_user(async_client):
    res = await async_client.post("/auth/register", json={
        "email": "user@test.com",
        "password": "test123",
        "name": "User Test"
    })
    assert res.status_code == 200
    assert res.json()["email"] == "user@test.com"

@pytest.mark.asyncio
async def test_login_user(async_client):
    res = await async_client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "test123"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()
