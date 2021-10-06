from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, JSON
from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    source = Column(String, nullable=True)
    reference = Column(String, nullable=True)
    description = Column(String, nullable=True)
    description_html = Column(String, nullable=True)
    original_link_to_item = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)
    categories = Column(JSON, nullable=True)
    images = Column(JSON, nullable=True)
    files = Column(JSON, nullable=True)
    comments = Column(JSON, nullable=True)
    cdn_images = Column(JSON, nullable=True)
