from sqlalchemy.orm import DeclarativeBase
from .models import *

from sqlalchemy.dialects.sqlite import insert as sqlite_insert
import os

# needs to import everything from all the models to ensure that the all
#    the tables are created
import argparse
import logging

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def simple_drop_database():
    Base.metadata.drop_all(engine)
    print("added all the tables")


def simple_create_database():
    Base.metadata.create_all(engine)
    print("added all the tables")


def main():
    parser = argparse.ArgumentParser(description="Database Management")
    parser.add_argument(
        "command", choices=["create", "drop"], help="Choose command: create or drop"
    )
    args = parser.parse_args()
    if args.command == "create":
        simple_create_database()
    elif args.command == "drop":
        simple_drop_database()


if __name__ == "__main__":
    main()
