"""Data repository interface for categories."""

from sqlalchemy.exc import SQLAlchemyError

from catalog_webapp.model.category import Category


class CategoryRepo():
    """The category repository interface."""

    def __init__(self, session_factory):
        """Constructor.

        session_factory -- sqlalchemy.orm.session.sessionmaker -
        The session factory used to create sessions for accessing the
        database.
        """
        self._sf = session_factory

    def get_by_id(self, cid):
        """Return the category with the given id.

        Keyword arguments:
        cid - int - the id of the category to retrieve. Required.

        Will return None if there is no category with the provided id.
        """
        session = self._sf()
        category = None
        try:
            category = session.query(Category).filter(Category.id == cid)\
                       .one_or_none()
        finally:
            session.close()
        return category

    def get_all(self):
        """Return all categories."""
        session = self._sf()
        categories = []
        try:
            categories = session.query(Category).all()
        finally:
            session.close()
        return categories

    def add(self, category):
        """Add a cateogry.

        Keyword arguments:
        category - catalog_webapp.model.Category - the category to add.
                   Required.
        """
        session = self._sf()
        try:
            session.add(category)
            session.commit()
            session.refresh(category)
            session.expunge(category)
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
