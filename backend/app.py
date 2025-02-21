from fastapi import FastAPI, Response
import secrets

app = FastAPI()

TOKEN_NAME = "user_token"

token_to_user_id = {}


@app.post("/login")
async def login(response: Response):
    user_id = None
    new_token = secrets.token_urlsafe(32)
    token_to_user_id[user_id] = new_token
    response.set_cookie(key=TOKEN_NAME, value=new_token)
    return {"success": True}


@app.post("/register")
async def register():
    return {"message": "Hello World"}


@app.get("/")
async def root():
    return {"message": "Hello World"}
