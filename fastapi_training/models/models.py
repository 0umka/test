from pydantic import BaseModel
from typing import List, Union, Optional
from datetime import datetime


class User(BaseModel):
 #   id: int
    name: str
    age: int
    is_adult: bool = False

class FeedBack(BaseModel):
    name: str
    message: str

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    is_subscribed: Union[bool, None] = None
    
class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float    

class Login(BaseModel):
    username: str
    password: str

class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool