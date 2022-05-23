from sqlalchemy.orm import Session
import pytest
from app import crud
from app.schemas.item import ItemCreate, ItemUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string

@pytest.mark.asyncio
async def test_create_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=title, description=description)
    user = await create_random_user(db)
    item = await crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=user["_id"])
    assert item["name"] == title
    assert item["description"] == description
    assert item["owner_id"] == str(user["_id"])

@pytest.mark.asyncio
async def test_get_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=title, description=description)
    user = await create_random_user(db)
    item = await crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=user["_id"])
    stored_item = await crud.item.get(db=db, id=item["_id"])
    assert stored_item
    assert item["_id"] == stored_item["_id"]
    assert item["name"] == stored_item["name"]
    assert item["description"] == stored_item["description"]
    assert item["owner_id"] == stored_item["owner_id"]

@pytest.mark.asyncio
async def test_update_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=title, description=description)
    user = await create_random_user(db)
    item = await crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=user["_id"])
    description2 = random_lower_string()
    item2 = await crud.item.update(db=db, db_obj=item, obj_in={"description": description2})
    assert item["_id"] == item2["_id"]
    assert item["name"] == item2["name"]
    assert item2["description"] == description2
    assert item["owner_id"] == item2["owner_id"]

@pytest.mark.asyncio
async def test_delete_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=title, description=description)
    user = await create_random_user(db)
    item = await crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=user["_id"])
    item2 = await crud.item.remove(db=db, id=item["_id"])
    item3 = await crud.item.get(db=db, id=item["_id"])
    assert item3 is None
    assert item2["_id"] == item["_id"]
    assert item2["name"] == title
    assert item2["description"] == description
    assert item2["owner_id"] == str(user["_id"])

