import pytest

@pytest.fixture
async def auth_header(async_client):
    await async_client.post(
        "/auth/register",
        json={"email": "test@ex.com", "password": "senha", "name": "Teste"},
    )
    resp = await async_client.post(
        "/auth/login",
        json={"email": "test@ex.com", "password": "senha"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_and_list_lists(async_client, auth_header):
    resp = await async_client.post(
        "/lists/", headers=auth_header, json={"name": "Minhas Armas"}
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Minhas Armas"

    resp = await async_client.get("/lists/", headers=auth_header)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(l["name"] == "Minhas Armas" for l in data)

@pytest.mark.asyncio
async def test_add_and_get_list_items(async_client, auth_header, monkeypatch):
    from sources.manager import get_item_from_sources

    class FakeItem:
        name = "Gladius"
        image_collection = "url"
        soldBy = []
        itemSummonInfoContainedIn = []

    monkeypatch.setattr(
        "sources.manager.get_item_from_sources", lambda item_id: FakeItem()
    )

    resp = await async_client.post(
        "/lists/", headers=auth_header, json={"name": "Test"}
    )
    list_id = resp.json()["id"]

    resp = await async_client.post(
        f"/lists/{list_id}/items",
        headers=auth_header,
        json={"items": [{"item_id": 1219, "quantity": 5}]},
    )
    assert resp.status_code == 201

    resp = await async_client.get(
        f"/lists/{list_id}/items", headers=auth_header
    )
    assert resp.status_code == 200
    items = resp.json()
    assert items[0]["item_id"] == 1219
    assert items[0]["qtd_item"] == 5
