import os
from sqlalchemy.orm import (
    CascadeOptions,
    Mapped,
    mapped_column,
    relationship,
    Session,
    declarative_base,
)
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Float,
    JSON,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    email: Mapped[String] = mapped_column(String(), primary_key=True)
    password_hash: Mapped[String] = mapped_column(String(), nullable=False)

    # may later add these
    # user_group_relationships: Mapped[list["UserGroupRelationships"]] = relationship(
    #     back_populates="user"
    # )


class BillingGroup(Base):
    __tablename__ = "billing_groups"
    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String(), nullable=False)

    # user_group_relationships: Mapped[list["BillingGroup"]] = relationship(
    #     back_populates="user"
    # )


class UserGroupRelationships(Base):
    __tablename__ = "user_group_relationships"
    user_email: Mapped[String] = mapped_column(
        String(), ForeignKey("users.email"), primary_key=True
    )
    group_id: Mapped[Integer] = mapped_column(
        Integer(), ForeignKey("billing_groups.id"), primary_key=True
    )


class Invoice(Base):
    __tablename__ = "invoices"
    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    group_id: Mapped[Integer] = mapped_column(
        Integer(), ForeignKey("billing_groups.id", ondelete="cascade")
    )
    total_invoice_cost: Mapped[Float] = mapped_column(Float(), nullable=False)
    is_settled: Mapped[Boolean] = mapped_column(
        Boolean(), nullable=False, default=False
    )
    is_outgoing: Mapped[Boolean] = mapped_column(Boolean(), nullable=False)
    item: Mapped[JSON] = mapped_column(JSON())
    details: Mapped[JSON] = mapped_column(JSON())


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
