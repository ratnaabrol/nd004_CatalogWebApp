"""Defines the default rdbms engine to use for this application."""

from sqlalchemy import create_engine


DEFAULT_ENGINE = create_engine("sqlite:///default_catalog.db")
