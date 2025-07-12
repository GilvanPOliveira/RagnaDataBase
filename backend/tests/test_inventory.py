import pytest

@pytest.mark.asyncio
async def test_inventory_flow(async_client):
    await async_client.post("/auth/register", json={
        "email": "inv@test.com", "password": "123456", "name": "Inv"
    })
    login = await async_client.post("/auth/login", json={
        "email": "inv@test.com", "password": "123456"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await async_client.post("/inventory/add", headers=headers, json={
        "item_id": 1219,
        "item_name": "Gladius",
        "image_collection": "img.png",
        "quantity": 3,
        "price": 5000
    })
    assert res.status_code == 200

    res = await async_client.get("/inventory/list", headers=headers)
    assert res.status_code == 200
    inventory_list = res.json()
    assert any(i["item_id"] == 1219 for i in inventory_list)

    res = await async_client.patch("/inventory/update/1219", headers=headers, json={
        "price": 4500.0,
        "quantity": 3
    })
    assert res.status_code == 200
    assert res.json()["message"] == "Item atualizado com sucesso."

    res = await async_client.delete("/inventory/remove/1219", headers=headers)
    assert res.status_code == 200
    assert "removido" in res.json()["message"].lower()  # ✔ Corrigido aqui
