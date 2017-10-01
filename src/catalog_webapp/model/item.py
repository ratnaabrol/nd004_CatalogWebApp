"""Code relating to the item entity."""

# pylint:disable=too-few-public-methods
# pylint:disable=invalid-name

from sqlalchemy import Column, DateTime, Integer, Text, Sequence, String
from sqlalchemy.schema import ForeignKey, UniqueConstraint
from sqlalchemy.sql.expression import func
from catalog_webapp.model.mapping_base import BASE


class Item(BASE):
    """Item entity."""
    __tablename__ = "items"

    id = Column(Integer, Sequence("items_id_seq"), autoincrement=True,
                primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    created_at_utc = \
        Column(DateTime, nullable=False, server_default=func.now())
    description = Column(Text)
    __table_args__ = (UniqueConstraint("category_id", "name"),)

    def _key(self):
        return (self.id, self.owner_id, self.category_id, self.name,
                self.created_at_utc, self.description)

    @staticmethod
    def _is_valid_(other):
        return (hasattr(other, "id") and
                hasattr(other, "owner_id") and
                hasattr(other, "category_id") and
                hasattr(other, "name") and
                hasattr(other, "created_at_utc") and
                hasattr(other, "description"))

    def __eq__(self, other):
        if not Item._is_valid_(other):
            return NotImplemented
        return self._key() == other._key()  # pylint:disable=protected-access

    def __lt__(self, other):
        if not Item._is_valid_(other):
            return NotImplemented
        return self._key() < other._key()  # pylint:disable=protected-access

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        key = self._key()
        template = ""
        for _ in range(len(key)):
            template = template + "[{}]"
        return template.format(*self._key())
