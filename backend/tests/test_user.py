import pytest

@pytest.mark.asyncio
async def test_me_update_delete(async_client):
    await async_client.post("/auth/register", json={
        "email": "user@test.com",
        "password": "test123",
        "name": "User"
    })

    login = await async_client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "test123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # GET /me
    res = await async_client.get("/users/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["email"] == "user@test.com"

    # PATCH /me
    res = await async_client.patch("/users/me", headers=headers, json={"name": "Novo Nome"})
    assert res.status_code == 200
    assert res.json()["name"] == "Novo Nome"

    # DELETE /me
    res = await async_client.delete("/users/me", headers=headers)
    assert res.status_code == 200
    assert "deletado com sucesso" in res.json()["message"]
