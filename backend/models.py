import os
from sqlalchemy.orm import (
    Mapped,
    validates,
    mapped_column,
    relationship,
    Session,
    declarative_base,
)
from dotenv import load_dotenv
from sqlalchemy import (
    ForeignKey,
    create_engine,
    Integer,
    String,
    Boolean,
    Float,
    JSON,
    Enum,
    DateTime,
    UniqueConstraint,
    ForeignKeyConstraint,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    email: Mapped[String] = mapped_column(String(), primary_key=True)
    password_hash: Mapped[String] = mapped_column(String(), nullable=False)


class BillingGroup(Base):
    __tablename__ = "billing_groups"
    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name = mapped_column(String(), nullable=False)


class UserGroupRelationships(Base):
    __tablename__ = "user_group_relationships"
    user_email = mapped_column(String(), primary_key=True)
    group_id = mapped_column(Integer(), primary_key=True)


class Invoice(Base):
    __tablename__ = "invoices"
    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    total_invoice_cost = mapped_column(Float(), nullable=False)
    is_settled = mapped_column(Boolean(), nullable=False, default=False)
    is_outgoing = mapped_column(Boolean(), nullable=False)
    items = mapped_column(JSON())
    details = mapped_column(JSON())


### Database connecction
# probably should go in a different place

# Database configuration
load_dotenv()
database_url = os.getenv("DATABASE_URL")
if database_url is None:
    raise Exception(
        "Database env variable not set. make a .env file with DATABASE_URL as the url to the postgres database"
    )
# Create the engine and session
engine = create_engine(database_url)
session = Session(engine)
###
