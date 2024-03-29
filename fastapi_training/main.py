from fastapi import FastAPI, Response, Cookie, Header
from test.fastapi_training.models.models import Product, Login, Todo
import secrets
from typing import Annotated
import asyncpg

app = FastAPI()

mas = []

@app.post("/product")
def inf_product(product: Product):
    mas.append({
        "id":product.product_id, 
        "name":product.name, 
        "category":product.category, 
        "price":product.price
        })
    return mas

@app.get("/product/{product_id}")
def product(product_id: int):
    return list(filter(lambda x: product_id == x["id"], mas))


@app.get("/products/search")
def search_product(keyword: str, category: str = None, limit: int = 10):
    result = list(filter(lambda x: keyword in x["name"], mas))
    if category:
        result = list(filter(lambda x: category in x["category"], result))
    return result[:limit]


people = {}

@app.post("/login")
def auth(response: Response, log: Login):
    global people
    token = secrets.token_hex(16)
    people = {"username":log.username, "password":log.password}
    people["session_token"] = token
    response.set_cookie(key="session_token", value=token, httponly=True)
    return {'message': 'cookie'}
    
@app.get("/user")
def is_right(session_token = Cookie()):
    print(people)
    if people["session_token"] == session_token:
        return people
    else:
        return "stfu"

@app.get("/headers")
async def read_items(user_agent: Annotated[str | None, Header()] = None, accept_language: Annotated[str | None, Header()] = None):
    if user_agent == None or accept_language == None:
        return "error 400"
    else: return {"User-agent": user_agent, "Accept-Language": accept_language}

#@app.post('/todo')
#async def things_todo(todo: Todo):
    
