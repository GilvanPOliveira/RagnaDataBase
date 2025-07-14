from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    DateTime, Boolean, func, UniqueConstraint
)
from sqlalchemy.orm import relationship
from db.session import Base

class User(Base):
    __tablename__ = "users"

    id        = Column(Integer, primary_key=True, index=True)
    email     = Column(String, unique=True, index=True, nullable=False)
    password  = Column(String, nullable=False)
    name      = Column(String, nullable=True)
    is_admin      = Column(Boolean, default=False)
    is_superadmin = Column(Boolean, default=False)

    inventories = relationship(
        "Inventory", back_populates="user", cascade="all, delete-orphan"
    )
    lists       = relationship(
        "List",      back_populates="user", cascade="all, delete-orphan"
    )

class Inventory(Base):
    __tablename__ = "inventories"

    id        = Column(Integer, primary_key=True, index=True)
    user_id   = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_id   = Column(Integer, nullable=False)
    item_name = Column(String,  nullable=False)
    image_collection = Column(String, nullable=True)
    quantity  = Column(Integer, default=1)
    price     = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="inventories")

class List(Base):
    __tablename__ = "lists"
    __table_args__ = (
        UniqueConstraint("user_id", "local_id", name="uq_user_local_id"),
    )

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    local_id   = Column(Integer, nullable=False, index=True)
    name       = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user  = relationship("User", back_populates="lists")
    items = relationship("ListItem", back_populates="list", cascade="all, delete-orphan")

class ListItem(Base):
    __tablename__ = "list_items"

    id         = Column(Integer, primary_key=True, index=True)
    list_id    = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"), nullable=False, index=True)
    item_id    = Column(Integer, nullable=False)
    quantity   = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    list = relationship("List", back_populates="items")

class Offer(Base):
    __tablename__ = "offers"

    id         = Column(Integer, primary_key=True, index=True)
    item_id    = Column(Integer, nullable=False, index=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    price      = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
