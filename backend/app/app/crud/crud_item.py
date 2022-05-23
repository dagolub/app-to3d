from typing import List, Any, TypeVar,Union, Dict
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from bson.objectid import ObjectId
from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from pydantic import BaseModel
from app.db.base_class import Base
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    async def get(self, db: Session, id: str) -> Any:
        item = await db["items"].find_one({"_id": ObjectId(id)})
        if item is None:
            return item
        return self.align_item(item)

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = []
        async for document in db["items"].find():
            result.append(self.align_item(document))
        return result

    async def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate, owner_id: int
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["owner_id"] = owner_id
        inserted_item = await db["items"].insert_one(obj_in_data)
        item = await db["items"].find_one({"_id": ObjectId(inserted_item.inserted_id)})
        return self.align_item(item)

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            db.query(self.model)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                db_obj[field] = update_data[field]
        await db["items"].update_one({"_id": ObjectId(db_obj['_id'])}, {'$set': update_data})
        item = await db["items"].find_one({"_id": ObjectId(db_obj['_id'])})
        return self.align_item(item)

    async def remove(self, db: Session, *, id: str) -> ModelType:
        item = await db["items"].find_one({"_id": ObjectId(id)})
        db["items"].delete_one({"_id": ObjectId(id)})
        return self.align_item(item)

    @staticmethod
    def align_item(current_item):
        if current_item is not None:
            for field in ["owner_id", "_id"]:
                current_item[field] = str(current_item[field])
            return current_item
        return item

item = CRUDItem(Item)
