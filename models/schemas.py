from pydantic import BaseModel
from datetime import date
class User(BaseModel):
    name: str
    email: str
    password: str
    contact :str


class Item(BaseModel):
    name: str
    description: str
    lostlocation: str
    foundlocation: str
    status: bool
    Date : date
    user_id: int

