import os
from sqlalchemy.orm import (
    Mapped,
    validates,
    mapped_column,
    relationship,
    Session,
    DeclarativeBase,
)
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

### Database connecction
# probably should go in a different place

# Database configuration
database_url = os.getenv("DATABASE_URL")
if database_url is None:
    raise Exception(
        "Database env variable not set. make a .env file with DATABASE_URL as the url to the postgres database"
    )
# Create the engine and session
engine = create_engine(database_url)
session = Session(engine)
###


class User(DeclarativeBase):
    __tablename__ = "users"
    email = mapped_column(String(), primary_key=True)
    password_hash = mapped_column(String(), nullable=False)


class BillingGroup(DeclarativeBase):
    __tablename__ = "billing_groups"
    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name = mapped_column(String(), nullable=False)


class UserGroupRelationships(DeclarativeBase):
    __tablename__ = "user_group_relationships"
    user_email = mapped_column(String(), primary_key=True)
    group_id = mapped_column(Integer(), primary_key=True)


class Invoice(DeclarativeBase):
    __tablename__ = "users"
    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    total_invoice_cost = mapped_column(Float(), nullable=False)
    is_settled = mapped_column(Boolean(), nullable=False, default=False)
    is_outgoing = mapped_column(Boolean(), nullable=False)
    items = mapped_column(JSON())
    details = mapped_column(JSON())
