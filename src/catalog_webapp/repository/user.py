"""Data repository interface for users."""

from sqlalchemy.exc import SQLAlchemyError

from catalog_webapp.model.auth_provider import AuthProvider
from catalog_webapp.model.user import User


class UserRepo():
    """The user repository interface."""

    def __init__(self, session_factory):
        """Constructor.

        session_factory -- sqlalchemy.orm.session.sessionmaker -
        The session factory used to create sessions for accessing the
        database.
        """
        self._sf = session_factory

    def add_user(self, user):
        """Add a user to the database.

        Keyword arguments:
        user -- catalog_webapp.model.user.User - the user to add to the
        database

        Exceptions:
        LookupError -- if the user already exists
        sqlalchemy.exc.SQLAlchemyError -- if an error occurs accessing the
        database
        """
        if not self.exists_by_username(user.username):
            session = self._sf()
            try:
                session.add(user)
                session.commit()
                session.refresh(user)
                session.expunge(user)
            except SQLAlchemyError:
                session.rollback()
                raise
            finally:
                session.close()
        else:
            raise LookupError

    def update_user(self, user):
        """Updates the user within the database.

        Keyword arguments:
        user -- catalog_webapp.model.user.User - the user to add to the
        database

        Exceptions:
        LookupError -- if the user does not already exists
        sqlalchemy.exc.SQLAlchemyError -- if an error occurs accessing the
        database
        """
        session = self._sf()
        found_user = self.get_by_username(user.username, user.provider)
        if found_user:
            try:
                user.id = found_user.id
                session.merge(user)
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                raise
            finally:
                session.close()
        else:
            raise LookupError

    def exists_by_username(self, username, provider=AuthProvider.local):
        """Return whether user with given properties exist.

        Keyword arguments:
        username -- string - the user name. Required.
        provider -- AuthProvider - the auth provider used to register this
                    user. Optional. Defaults to AuthProvider.local.
        """
        session = self._sf()
        count = 0
        try:
            count = session.query(User)\
             .filter(User.username == username, User.provider == provider)\
             .count()
        finally:
            session.close()
        return count != 0

    def get_by_username(self, username, provider=AuthProvider.local):
        """Return the user with the given username and provider.

        Keyword arguments:
        username -- string - the user name. Required.
        provider -- AuthProvider - the auth provider used to register this
                    user. Optional. Defaults to AuthProvider.local.
        """
        user = None
        session = self._sf()
        try:
            user = session.query(User)\
              .filter(User.username == username, User.provider == provider)\
              .one_or_none()
        finally:
            session.close()
        return user

    def get_by_email(self, email, provider=AuthProvider.local):
        """Return the user with the given email and provider.

        Keyword arguments:
        email -- string - the user's email address. Required.
        provider -- AuthProvider - the auth provider used to register this
                    user. Optional. Defaults to AuthProvider.local.
        """
        user = None
        session = self._sf()
        try:
            user = session.query(User)\
              .filter(User.email == email, User.provider == provider)\
              .one_or_none()
        finally:
            session.close()
        return user

    def get_all_users(self):
        """Get all users as a list of users.

        Will return an empty list if no users exist.
        """
        session = self._sf()
        try:
            return session.query(User).all()
        finally:
            session.close()

        return []
