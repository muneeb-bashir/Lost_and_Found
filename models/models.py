from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.types import Date
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    contact=Column(String, unique=True)
    user_items= relationship('Item', backref='user', cascade="all, delete-orphan", lazy='dynamic')


class Item(Base):
    __tablename__=" items"

    id=Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    lost_location = Column(String)
    found_location = Column(String)
    status = Column(Boolean, default=False)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    