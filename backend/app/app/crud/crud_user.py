from typing import Any, Dict, Optional, Union
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db, email: str) -> Optional[User]:
        return await db["users"].find_one({"email": email})

    async def create(self, db, obj_in: dict) -> User:
        obj_in = jsonable_encoder(obj_in)
        db_obj = {
            "email": obj_in["email"],
            "hashed_password": get_password_hash(obj_in["password"]),
            "full_name": obj_in.get("full_name"),
            "is_superuser": obj_in.get("is_superuser") or False,
            "is_active": True
        }
        obj = await db["users"].insert_one(document=db_obj)
        return await db["users"].find_one({"_id": ObjectId(obj.inserted_id)})

    async def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        obj_in = jsonable_encoder(obj_in)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        if 'email' in update_data:
            del update_data['email']
        await db["users"].update_one({"_id": db_obj['_id']},{'$set': update_data})
        return await db["users"].find_one({"_id": db_obj['_id']})

    async def authenticate(self, db: AsyncIOMotorClient, *, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user["is_active"]

    def is_superuser(self, user: User) -> bool:
        return user["is_superuser"]


user = CRUDUser(User)
