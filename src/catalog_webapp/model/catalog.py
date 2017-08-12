"""Code relating to the catalog entity."""

# pylint:disable=too-few-public-methods
# pylint:disable=invalid-name

from sqlalchemy import Column, DateTime, Integer, Text, Sequence, String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.expression import func
from catalog_webapp.model.mapping_base import BASE


class Catalog(BASE):
    """Catalog entity."""
    __tablename__ = "catalogs"

    id = Column(Integer, Sequence("catalogs_id_seq"), autoincrement=True,
                primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    created_at_utc = \
        Column(DateTime, nullable=False, server_default=func.now())
    description = Column(Text)
