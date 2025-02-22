from .models import *

from sqlalchemy.dialects.sqlite import insert as sqlite_insert
import os

# needs to import everything from all the models to ensure that the all
#    the tables are created
import argparse
import logging

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def simple_create_database():
    Base.metadata.create_all(engine)
    print("added all the tables")


def main():
    simple_create_database()


if __name__ == "__main__":
    main()
