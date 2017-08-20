"""Creates the database for this application."""
import argparse
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from catalog_webapp.model.mapping_base import BASE
from catalog_webapp.db.default_engine import DEFAULT_ENGINE

# import the models so that the BASE is populated
from catalog_webapp.model import user  # pylint:disable-msg=unused-import


def get_dbstr_from_args():
    """Returns the db connect string from the command line arguments."""
    parser = argparse.ArgumentParser(
        description="Create database compatible with this application.")
    parser.add_argument("--dbstr", type=str, default=None,
                        help="the connection string for the db. Optional. " +
                        "If omitted will create a default sqlite " +
                        "database in the current directory.")
    args = parser.parse_args()
    return args.dbstr


def main():
    """Script to create SQLite database for this application"""
    engine = DEFAULT_ENGINE
    dbstr = get_dbstr_from_args()
    try:
        if dbstr:
            engine = create_engine(dbstr)

        BASE.metadata.create_all(engine)
        print("Database created.")
    except SQLAlchemyError as exp:
        print("Unable to create database.")
        print("Error: {}".format(exp))


if __name__ == "__main__":
    main()
