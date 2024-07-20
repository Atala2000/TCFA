from pydantic import BaseModel
from app.models.base import Items, Orders

class ItemBase(BaseModel):
    price: int
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

class UserBase(BaseModel):
    email: str

class UserCreate(BaseModel):
    password: str
    phone: int

class User(BaseModel):
    id: int
    orders: list[Orders]

class OrderBase(BaseModel):
    time: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    owner: User
    item: Items

class 