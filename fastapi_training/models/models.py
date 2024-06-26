from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
 #   id: int
    username: str
    password: str
    role: Optional[str] = None
 #   is_adult: bool = False

class FeedBack(BaseModel):
    name: str
    message: str

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    is_subscribed: Optional[bool] = None
    
class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float    

class Login(BaseModel):
    username: str
    password: str

class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Todo_return(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    id: Optional[int]
