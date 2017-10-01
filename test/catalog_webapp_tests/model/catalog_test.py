"""Tests for the catalog model"""

import unittest
import datetime

from catalog_webapp.model.catalog import Catalog

# pylint:disable=invalid-name
# pylint:disable=missing-docstring

class CatalogTest(unittest.TestCase):
    """Tester"""

    def test_equals_returns_true_for_same_object(self):
        now = datetime.datetime.now()
        c = Catalog(id=1, owner_id=1, name="A", created_at_utc=now,
                    description="F")
        self.assertTrue(c == c)


    def test_equals_returns_true_for_equal_objects(self):
        now = datetime.datetime.now()
        c1 = Catalog(id=1, owner_id=1, name="A", created_at_utc=now,
                     description="F")
        c2 = Catalog(id=1, owner_id=1, name="A", created_at_utc=now,
                     description="F")
        self.assertTrue(c1 == c2)

    def test_equals_returns_false_for_unequal_objects(self):
        now = datetime.datetime.now()
        c1 = Catalog(id=1, owner_id=1, name="A", created_at_utc=now,
                     description="F")
        c2 = Catalog(id=1, owner_id=2, name="B", created_at_utc=now,
                     description="G")
        self.assertFalse(c1 == c2)

    def test_hash_is_consistent_when_called_many_time(self):
        now = datetime.datetime.now()
        c = Catalog(id=1, owner_id=1, name="A", created_at_utc=now,
                    description="F")
        self.assertEqual(hash(c), hash(c))

    def test_hash_is_consistent_for_equal_objects(self):
        now = datetime.datetime.now()
        c1 = Catalog(id=1, owner_id=1, name="A", created_at_utc=now,
                     description="F")
        c2 = Catalog(id=1, owner_id=1, name="A", created_at_utc=now,
                     description="F")
        self.assertTrue(hash(c1) == hash(c2))
