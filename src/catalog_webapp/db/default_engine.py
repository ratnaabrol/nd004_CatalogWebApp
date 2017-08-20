"""Defines the default rdbms engine to use for this application."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DEFAULT_ENGINE = create_engine("sqlite:///default_catalog.db")
SESSION_FACTORY = sessionmaker(bind=DEFAULT_ENGINE)
