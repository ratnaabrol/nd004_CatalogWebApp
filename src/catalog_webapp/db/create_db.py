"""Creates the database for this application."""

from catalog_webapp.db.default_engine import DEFAULT_ENGINE
from catalog_webapp.model.mapping_base import BASE

# import the models so that the BASE is populated
from catalog_webapp.model import user  # pylint:disable-msg=unused-import


def main():
    """Script to create SQLite database for this application"""
    engine = DEFAULT_ENGINE
    BASE.metadata.create_all(engine)


if __name__ == "__main__":
    main()
