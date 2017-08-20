"""Defines the rdbms engine to use for testing this application."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


TEST_ENGINE = create_engine("sqlite:///test_catalog.db")
TEST_SESSION_FACTORY = sessionmaker(bind=TEST_ENGINE)
