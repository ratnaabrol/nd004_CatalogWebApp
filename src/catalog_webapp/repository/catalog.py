"""Data repository interface for catalogues."""

from sqlalchemy.exc import SQLAlchemyError

from catalog_webapp.model.catalog import Catalog


class CatalogRepo():
    """The user repository interface."""

    def __init__(self, session_factory):
        """Constructor.

        session_factory -- sqlalchemy.orm.session.sessionmaker -
        The session factory used to create sessions for accessing the
        database.
        """
        self._sf = session_factory

    def get_by_id(self, cid):
        """Return the catalog with the given id.

        Keyword arguments:
        cid - int - the id of the catalog to retrieve. Required.

        Will return None if there is no catalog with the provided id.
        """
        session = self._sf()
        catalog = None
        try:
            catalog = session.query(Catalog).filter(Catalog.id == cid)\
                      .one_or_none()
        finally:
            session.close()
        return catalog

    def get_all(self):
        """Return all catalogs."""
        session = self._sf()
        catalogs = []
        try:
            catalogs = session.query(Catalog).all()
        finally:
            session.close()
        return catalogs

    def add(self, catalog):
        """Add a catalog.

        Keyword arguments:
        catalog - catalog_webapp.model.Catalog - the catalog to add. Required.
        """
        session = self._sf()
        try:
            session.add(catalog)
            session.commit()
            session.refresh(catalog)
            session.expunge(catalog)
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
