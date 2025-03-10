from fastapi import FastAPI, File, HTTPException, Response, Request, UploadFile
import json
from fastapi.responses import JSONResponse, FileResponse
from openai import OpenAI
from starlette.types import ExceptionHandler
import os
from backend.db.models import *
from sqlalchemy import select
import shutil
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
import hashlib
import secrets
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow the front-end URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.mount(
    "/invoice-uploads", StaticFiles(directory="invoice-pdfs"), name="invoice-pdfs"
)

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
file_path_count = 0
email_to_filepaths: dict[str, tuple[int, list[str]]] = {}
file_path_num_to_email: dict[int, str] = {}


class UploadInfo(BaseModel):
    name: str
    is_outgoing: bool


@app.post("/invoice-upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    global file_path_count
    # token = request.cookies.get(TOKEN_NAME)
    # if token is None:
    #     return {"success": False, "message": "you need to be logged in"}
    # user_email = token_to_user_id.get(token)
    # if user_email is None:
    #     return {"success": False, "message": "your login token is expired log in again"}
    # assert file.filename is not None
    user_email = "test"
    print(file.content_type)
    if user_email not in email_to_filepaths:
        email_to_filepaths[user_email] = (file_path_count, [])
        file_path_num_to_email[file_path_count] = user_email
        file_path_count += 1
    user_num = email_to_filepaths[user_email][0]
    dir_path = os.path.join(
        "invoice-pdfs",
        str(user_num),
    )
    os.makedirs(dir_path, exist_ok=True)

    invoice_num = email_to_filepaths[user_email][1]
    file_path = os.path.join(
        dir_path,
        f"{len(invoice_num)}.pdf",
    )
    email_to_filepaths[user_email][1].append(file_path)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    client = OpenAI(
        base_url="https://kevinbeutler2003.ap.xpressai.cloud/api/lexi/",
        api_key=os.getenv("XPRESS_API_KEY"),
    )

    chat = client.chat.completions.create(
        model="Lexi",  # Available models: Lexi, LexiOnboarding
        messages=[
            {
                "role": "user",
                "content": f"The URL of the invoice is: https://xpress-hackathon.onrender.com/invoice-uploads/{user_num}/{invoice_num}.pdf Please download the pdf and return the json of it's information.",
            }
        ],
    )
    out = chat.choices[-1].message.content
    assert out is not None
    lines = out.splitlines()
    start = lines.index("```json")
    end = lines.index("```")

    invoice_json = json.loads("".join(lines[start + 1 : end]))
    invoice = Invoice(
        group_id=1,  # would need to be fixed
        total_invoice_cost=invoice_json.get("total_invoice_cost", 0),
        is_settled=invoice_json.get("is_settled", False),
        is_outgoing=invoice_json.get("is_outgoing", True),
        item=invoice_json.get("item", invoice_json.get("items", [])),
        details=invoice_json.get("details", []),
    )
    session.add(invoice)
    session.commit()

    return {"message": "PDF file uploaded and saved successfully"}


@app.get("/send-email")
async def send_email():
    client = OpenAI(
        base_url="https://kevinbeutler2003.ap.xpressai.cloud/api/lexi/",
        api_key=os.getenv("XPRESS_API_KEY"),
    )

    _ = client.chat.completions.create(
        model="Lexi",  # Available models: Lexi, LexiOnboarding
        messages=[
            {
                "role": "user",
                # TODO make it upload a certain pdf
                "content": f"The URL of the invoice is: https://xpress-hackathon.onrender.com/invoice-uploads/0/0.pdf Please parse the pdf and return the json of it's information formatted.",
            }
        ],
    )

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
    response.set_cookie(
        key=TOKEN_NAME,
        value=new_token,
        httponly=False,
        samesite=None,
        secure=True,
    )
    return {"success": True, "login_token": new_token}


class NewGroupsInfo(BaseModel):
    name: str


@app.get("/invoice-uploads")
async def get_invoices_pdf(request: Request):
    """returns the invoices without the domain name"""
    # token = request.cookies.get(TOKEN_NAME)
    # if token is None:
    #     return {"success": False, "message": "you need to be logged in"}
    # user_email = token_to_user_id.get(token)
    # if user_email is None:
    #     return {"success": False, "message": "your login token is expired log in again"}
    # if user_email not in email_to_filepaths:
    #     return []
    user_email = "test"
    user_num, file_paths = email_to_filepaths[user_email]
    invoice_links: list[str] = []
    for invoice_num in range(len(file_paths)):
        invoice_links.append(f"invoice-uploads/{user_num}/{invoice_num}.pdf")
    return invoice_links


@app.post("/groups")
async def make_group(group_info: NewGroupsInfo, request: Request):
    # token = request.cookies.get(TOKEN_NAME)
    # if token is None:
    #     return {"success": False, "message": "you need to be logged in"}
    # user_email = token_to_user_id.get(token)
    # if user_email is None:
    #     return {"success": False, "message": "your login token is expired log in again"}
    user_email = "test"
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
    # token = request.cookies.get(TOKEN_NAME)
    # if token is None:
    #     return {"success": False, "message": "you need to be logged in"}
    # user_email = token_to_user_id.get(token)
    # if user_email is None:
    #     return {"success": False, "message": "your login token is expired log in again"}
    user_email = "test"

    select_get_groups = (
        select(BillingGroup)
        .join(UserGroupRelationships)
        .filter(UserGroupRelationships.user_email == user_email)
    )
    return session.scalars(select_get_groups).all()


@app.delete("/groups")
async def delete_group(request: Request, group_info: GetGroupsInfo):
    # token = request.cookies.get(TOKEN_NAME)
    # if token is None:
    #     return {"success": False, "message": "you need to be logged in"}
    # user_email = token_to_user_id.get(token)
    # if user_email is None:
    #     return {"success": False, "message": "your login token is expired log in again"}
    get_user_group = select(UserGroupRelationships).filter(
        UserGroupRelationships.user_email == "test"
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


@app.get("/invoice")
async def get_invoice(request: Request):
    get_invoice_info = select(Invoice)
    return session.scalars(get_invoice_info).all()


@app.delete("/invoice")
async def delete_invoice(request: Request, get_invoices: GetInvoiceInfo):
    # token = request.cookies.get(TOKEN_NAME)
    # if token is None:
    #     return {"success": False, "message": "you need to be logged in"}
    # user_email = token_to_user_id.get(token)
    #
    # if user_email is None:
    #     return {"success": False, "message": "your login token is expired log in again"}
    user_email = "test"

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
