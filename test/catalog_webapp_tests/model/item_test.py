"""Tests for the category model"""

import unittest
import datetime

from catalog_webapp.model.item import Item

# pylint:disable=invalid-name
# pylint:disable=missing-docstring

class ItemTest(unittest.TestCase):
    """Tester"""

    def test_equals_returns_true_for_same_object(self):
        now = datetime.datetime.now()
        i = Item(id=1, owner_id=1, category_id=1, name="A",
                 created_at_utc=now, description="F")
        self.assertTrue(i == i)


    def test_equals_returns_true_for_equal_objects(self):
        now = datetime.datetime.now()
        i1 = Item(id=1, owner_id=1, category_id=1, name="A",
                  created_at_utc=now, description="F")
        i2 = Item(id=1, owner_id=1, category_id=1, name="A",
                  created_at_utc=now, description="F")
        self.assertTrue(i1 == i2)

    def test_equals_returns_false_for_unequal_objects(self):
        now = datetime.datetime.now()
        i1 = Item(id=1, owner_id=1, category_id=1, name="A",
                  created_at_utc=now, description="F")
        i2 = Item(id=1, owner_id=2, category_id=2, name="B",
                  created_at_utc=now, description="G")
        self.assertFalse(i1 == i2)

    def test_hash_is_consistent_when_called_many_time(self):
        now = datetime.datetime.now()
        i = Item(id=1, owner_id=1, category_id=1, name="A",
                 created_at_utc=now, description="F")
        self.assertEqual(hash(i), hash(i))

    def test_hash_is_consistent_for_equal_objects(self):
        now = datetime.datetime.now()
        i1 = Item(id=1, owner_id=1, category_id=1, name="A",
                  created_at_utc=now, description="F")
        i2 = Item(id=1, owner_id=1, category_id=1, name="A",
                  created_at_utc=now, description="F")
        self.assertTrue(hash(i1) == hash(i2))
