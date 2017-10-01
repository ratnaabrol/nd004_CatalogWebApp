"""Tests for the catalog model"""

import unittest
import datetime

from catalog_webapp.model.user import User
from catalog_webapp.model.auth_provider import AuthProvider

# pylint:disable=invalid-name
# pylint:disable=missing-docstring

class UserTest(unittest.TestCase):
    """Tester"""

    def test_equals_returns_true_for_same_object(self):
        now = datetime.datetime.now()
        c = User(id=1, username="bob", provider=AuthProvider.local,
                 email="bob@bob", joined_at_utc=now, active=True,
                 admin=False)
        self.assertTrue(c == c)


    def test_equals_returns_true_for_equal_objects(self):
        now = datetime.datetime.now()
        c1 = User(id=1, username="bob", provider=AuthProvider.local,
                  email="bob@bob", joined_at_utc=now, active=True,
                  admin=False)
        c2 = User(id=1, username="bob", provider=AuthProvider.local,
                  email="bob@bob", joined_at_utc=now, active=True,
                  admin=False)
        self.assertTrue(c1 == c2)

    def test_equals_returns_false_for_unequal_objects(self):
        now = datetime.datetime.now()
        c1 = User(id=1, username="bob", provider=AuthProvider.local,
                  email="bob@bob", joined_at_utc=now, active=True,
                  admin=False)
        c2 = User(id=2, username="tony", provider=AuthProvider.local,
                  email="tony@tony", joined_at_utc=now, active=True,
                  admin=False)
        self.assertFalse(c1 == c2)

    def test_hash_is_consistent_when_called_many_time(self):
        now = datetime.datetime.now()
        c = User(id=1, username="bob", provider=AuthProvider.local,
                 email="bob@bob", joined_at_utc=now, active=True,
                 admin=False)
        self.assertEqual(hash(c), hash(c))

    def test_hash_is_consistent_for_equal_objects(self):
        now = datetime.datetime.now()
        c1 = User(id=1, username="bob", provider=AuthProvider.local,
                  email="bob@bob", joined_at_utc=now, active=True,
                  admin=False)
        c2 = User(id=1, username="bob", provider=AuthProvider.local,
                  email="bob@bob", joined_at_utc=now, active=True,
                  admin=False)
        self.assertTrue(hash(c1) == hash(c2))
