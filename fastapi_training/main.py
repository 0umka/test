from fastapi import FastAPI, HTTPException
from databases import Database
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

DATABASE_URL = "postgresql://user:password@localhost/dbname"

database = Database(DATABASE_URL)


class UserCreate(BaseModel):
    username: str
    email: str


class UserReturn(BaseModel):
    username: str
    email: str
    id: Optional[int] = None


@app.on_event("startup")
async def startup_database():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()
    
    
@app.post("/users/", response_model=UserReturn)
async def create_user(user: UserCreate):
    query = "INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id"
    values = {"username": user.username, "email": user.email}
    try:
        user_id = await database.execute(query=query, values=values)
        return {**user.dict(), "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create user")