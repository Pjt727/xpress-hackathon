from fastapi import FastAPI, Response, Request
from .models import *
from sqlalchemy import select
from pydantic import BaseModel
import hashlib
import secrets

app = FastAPI()

TOKEN_NAME = "user_token"


def hash_password(password):
    # Convert the password to bytes
    password_bytes = password.encode("utf-8")
    # Create a new SHA-256 hash object
    sha256 = hashlib.sha256()
    # Update the hash object with the password bytes
    sha256.update(password_bytes)
    # Get the hashed password in hexadecimal format
    hashed_password = sha256.hexdigest()
    return hashed_password


token_to_user_id = {}


class LoginInfo(BaseModel):
    email: str
    password: str



@app.post("/login")
async def login(login_info: LoginInfo, response: Response):
    select_query = select(User).filter(User.email == login_info.email)
    user = session.scalar(select_query)
    if user is None:
        return {"success": False, "message": "Auth failed"}
    if user.password_hash != hash_password(login_info.password):
        return {"success": False, "message": "Auth failed"}
    # at this point the user logged in correctly
    new_token = secrets.token_urlsafe(32)
    token_to_user_id[new_token] = user.email
    response.set_cookie(key=TOKEN_NAME, value=new_token)
    return {"success": True}

class Groups(BaseModel):
    id: int
    name: str


@app.post("/MakeGroups")
async def makeGroup(group_info: Groups, user_info: User,  response: Response):
    group = BillingGroup(
        id = group_info.id,
        name = group_info.name
    )
    user = User(
        id = user_info.email,
        email = user_info.email
    )
    new_token = secrets.token_urlsafe(32)
    token_to_user_id[new_token] = user.email
    response.set_cookie(key=TOKEN_NAME, value=new_token)
    session.add(group)
    session.commit()
    return {"success": True}


@app.post("/DeleteGroups")
async def deleteGroup(group_info: Groups, user_info: User,  response: Response):
    group = BillingGroup(
        id = group_info.id,
        name = group_info.name
    )
    user = User(
        id = user_info.email,
        email = user_info.email
    )
    new_token = secrets.token_urlsafe(32)
    token_to_user_id[new_token] = user.email
    response.set_cookie(key=TOKEN_NAME, value=new_token)
    session.delete(group)
    session.commit()
    return {"success": True, "message": "record deleted successfully"}

    
    
class RegistrationInfo(BaseModel):
    email: str
    password: str


@app.post("/register")
async def register(registration_info: RegistrationInfo, response: Response):
    # email: Mapped[String] = mapped_column(String(), primary_key=True)
    # password_hash: Mapped[String] = mapped_column(String(), nullable=False)
    user = User(
        email=registration_info.email,
        password_hash=hash_password(registration_info.password),
    )

    session.add(user)
    session.commit()
    new_token = secrets.token_urlsafe(32)
    token_to_user_id[new_token] = user.email
    response.set_cookie(key=TOKEN_NAME, value=new_token)
    return {"success": True}


@app.get("/")
async def root():
    return {"message": "Hello World"}
