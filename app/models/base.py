from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.backend.session import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    phone = Column(Integer, nullable=False)

    orders = relationship('Orders', back_populates='owner')

class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    description = Column(String, nullable=False)

    orders = relationship('Orders', back_populates='item')

class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('items.id'))

    owner = relationship("User", back_populates="orders")
    item = relationship("Items", back_populates="orders")
