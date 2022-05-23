from typing import Optional
from bson.objectid import ObjectId
from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    name: Optional[str] = None
    source: Optional[str] = None
    reference: Optional[str] = None
    description: Optional[str] = None
    description_html: Optional[str] = None
    original_link_to_item: Optional[str] = None
    tags: list = []
    categories: list = []
    images: list = []
    files: list = []
    comments: list = []
    cdn_images: list = []


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass

# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    _id: str
    owner_id: str

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
