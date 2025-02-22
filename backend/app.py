from fastapi import FastAPI, File, HTTPException, Response, Request, UploadFile
from fastapi.responses import JSONResponse
from starlette.types import ExceptionHandler
from backend.db.models import *
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
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


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded PDF file to a specified location
    return {"message": "PDF file uploaded and saved successfully"}


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
async def get_groups(request: Request):
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
    return session.scalars(select_get_groups).all()


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


class InvoiceInfo(BaseModel):
    group_id: int
    total_invoice_cost: float
    is_settled: bool
    is_outgoing: bool
    item: list[dict]
    details: list[dict]


class GetInvoiceInfo(BaseModel):
    id: int


@app.post("/invoice")
async def invoice(new_invoice: InvoiceInfo, response: Response):
    invoice = Invoice(
        total_invoice_cost=new_invoice.total_invoice_cost,
        group_id=new_invoice.group_id,
        is_settled=new_invoice.is_settled,
        is_outgoing=new_invoice.is_outgoing,
        item=new_invoice.item,
        details=new_invoice.details,
    )

    session.add(invoice)
    session.commit()
    return {"success": True}


@app.delete("/invoice")
async def delete_invoice(request: Request, get_invoices: GetInvoiceInfo):
    token = request.cookies.get(TOKEN_NAME)
    if token is None:
        return {"success": False, "message": "you need to be logged in"}
    user_email = token_to_user_id.get(token)

    if user_email is None:
        return {"success": False, "message": "your login token is expired log in again"}

    get_invoice_info = (
        select(Invoice)
        .filter(Invoice.id == get_invoices.id)
        .join(BillingGroup)
        .join(UserGroupRelationships)
        .filter(UserGroupRelationships.user_email == user_email)
    )

    invoice_record = session.scalar(get_invoice_info)
    if invoice_record is None:
        return {
            "success": False,
            "message": "No such record exists",
        }
    session.delete(invoice_record)
    session.commit()
    return {"success": True, "message": "record deleted successfully"}


def rollback(request: Request, exc: HTTPException):
    session.rollback()
    return JSONResponse({"success": False, "message": "interal database error"})


app.add_exception_handler(SQLAlchemyError, rollback)  # pyright: ignore


@app.get("/")
async def root():
    return {"message": "Hello World"}
