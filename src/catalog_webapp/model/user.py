"""Code relating to the user entity"""

# pylint:disable=too-few-public-methods
# pylint:disable=invalid-name

from functools import total_ordering
from sqlalchemy import (Boolean, Column, DateTime, Enum, Integer, Sequence,
                        String)
from sqlalchemy.sql.expression import func
from catalog_webapp.model.mapping_base import BASE
from catalog_webapp.model.auth_provider import AuthProvider


@total_ordering
class User(BASE):
    """User entity."""
    __tablename__ = "users"

    id = Column(Integer, Sequence("users_id_seq"), autoincrement=True,
                primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    provider = Column(Enum(AuthProvider), nullable=False,
                      default=AuthProvider.local)
    email = Column(String(100), unique=True, nullable=False)
    joined_at_utc = Column(DateTime, nullable=False, server_default=func.now())
    active = Column(Boolean, nullable=False, default=False)
    admin = Column(Boolean, nullable=False, default=False)


    def _key(self):
        return (self.id, self.username, self.provider, self.email)

    @staticmethod
    def _is_valid_(other):
        return (hasattr(other, "id") and
                hasattr(other, "username") and
                hasattr(other, "provider") and
                hasattr(other, "email"))

    def __eq__(self, other):
        if not User._is_valid_(other):
            return NotImplemented
        return self._key() == other._key()  # pylint:disable=protected-access

    def __lt__(self, other):
        if not User._is_valid_(other):
            return NotImplemented
        return self._key() < other._key()  # pylint:disable=protected-access

    def __hash__(self):
        return hash(self._key())
