"""Code relating to the user entity"""

# pylint:disable=too-few-public-methods
# pylint:disable=invalid-name

from sqlalchemy import Column, Integer, String, Sequence, DateTime, Boolean
from sqlalchemy.sql.expression import func
from catalog_webapp.model.mapping_base import BASE


class User(BASE):
    """User entity."""
    __tablename__ = "users"

    id = Column(Integer, Sequence("users_id_seq"), autoincrement=True,
                primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    joined_at_utc = Column(DateTime, nullable=False, server_default=func.now())
    active = Column(Boolean, nullable=False, default=False)
