import pytest

@pytest.mark.asyncio
async def test_get_item_by_id(async_client):
    res = await async_client.get("/item/1219")
    assert res.status_code == 200
    assert res.json()["id"] == 1219

@pytest.mark.asyncio
async def test_search_item(async_client):
    res = await async_client.get("/search?name=gladius")
    assert res.status_code == 200
    assert isinstance(res.json()["results"], list)
