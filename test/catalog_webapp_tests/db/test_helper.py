"""Module containing helper classes for test interacting with the database."""


class DbTestHelper():
    """Helper class for database testing."""

    def __init__(self, engine, metadata, session_factory):
        """Constructor.

        Keywork arguments:
        engine -- sqlalchemy.engine.Engine - engine with which to connect to
        the database.
        metadata -- sqlalchemy.schema.MetaData - database schema
        session_factory -- sqlalchemy.orm.session.sessionmaker -
        The session factory used to create sessions for accessing the
        database."""
        self._engine = engine
        self._metadata = metadata
        self._sf = session_factory

    def reset_database(self):
        """Empty database of data and recreates schema"""
        self._metadata.drop_all(self._engine)
        self._metadata.create_all(self._engine)
