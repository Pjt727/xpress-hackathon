from backend.models import *
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.dialects.sqlite import insert as sqlite_insert
import os

# needs to import everything from all the models to ensure that the all
#    the tables are created
import argparse
import logging

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def simple_create_database():
    DeclarativeBase.metadata.create_all(engine)


def main():
    simple_create_database()


if __name__ == "__main__":
    simple_create_database()
