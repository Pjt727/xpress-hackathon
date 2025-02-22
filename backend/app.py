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


class NewGroupsInfo(BaseModel):
    name: str


@app.post("/groups")
async def make_group(group_info: NewGroupsInfo, request: Request):
    token = request.cookies.get(TOKEN_NAME)
    if token is None:
        return {"success": False, "message": "you need to be logged in"}
    user_email = token_to_user_id.get(token)
    if user_email is None:
        return {"success": False, "message": "your login token is expired log in again"}
    group = BillingGroup(name=group_info.name)
    session.add(group)
    session.flush()
    group_relationship = UserGroupRelationships(
        user_email=user_email, group_id=group.id
    )
    session.add(group_relationship)
    session.commit()
    return {"success": True}


class GetGroupsInfo(BaseModel):
    id: str


@app.get("/groups")
async def get_groups(group_info: GetGroupsInfo, request: Request):
    token = request.cookies.get(TOKEN_NAME)
    if token is None:
        return {"success": False, "message": "you need to be logged in"}
    user_email = token_to_user_id.get(token)
    if user_email is None:
        return {"success": False, "message": "your login token is expired log in again"}

    select_get_groups = (
        select(BillingGroup)
        .join(UserGroupRelationships)
        .filter(UserGroupRelationships.user_email == user_email)
    )
    return session.scalars(select_get_groups)


@app.delete("/groups")
async def delete_group(request: Request, group_info: GetGroupsInfo):
    token = request.cookies.get(TOKEN_NAME)
    if token is None:
        return {"success": False, "message": "you need to be logged in"}
    user_email = token_to_user_id.get(token)
    if user_email is None:
        return {"success": False, "message": "your login token is expired log in again"}
    get_user_group = select(UserGroupRelationships).filter(
        UserGroupRelationships.user_email == user_email
    )
    relationship_to_group = session.scalar(get_user_group)
    if relationship_to_group is None:
        return {
            "success": False,
            "message": "you do not own that group so you cannot delete it",
        }
    group = BillingGroup(id=group_info.id)
    session.delete(group)
    session.commit()
    return {"success": True, "message": "record deleted successfully"}

@app.delete("/invoice")
async def delete_invoice(invoice_info: InvoiceInfo, response: Response):

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


class Invoice(Base):
    __tablename__ = "invoices"
    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    total_invoice_cost = mapped_column(Float(), nullable=False)
    is_settled = mapped_column(Boolean(), nullable=False, default=False)
    is_outgoing = mapped_column(Boolean(), nullable=False)
    items = mapped_column(JSON())
    details = mapped_column(JSON())

class InvoiceInfo(BaseModel):
    id: int
    total_invoice_cost: float
    is_settled : bool
    is_outgoing : bool
    items  : JSON
    details : JSON
    
    
@app.delete("/invoice")
async def delete_invoice(invoice_info: InvoiceInfo, response: Response):
    

@app.get("/")
async def root():
    return {"message": "Hello World"}
