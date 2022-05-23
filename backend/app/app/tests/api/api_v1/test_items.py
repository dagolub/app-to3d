from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.tests.utils.item import create_random_item
import pytest


@pytest.mark.asyncio
async def test_create_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"name": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/items/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    # assert "id" in content
    assert "owner_id" in content

@pytest.mark.asyncio
async def test_read_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    item = await create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/items/{item['_id']}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == item["name"]
    assert content["description"] == item["description"]
    # assert content["id"] == item._id
    assert content["owner_id"] == item["owner_id"]

@pytest.mark.asyncio
async def test_read_items(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    item = await create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/items/", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) > 1
