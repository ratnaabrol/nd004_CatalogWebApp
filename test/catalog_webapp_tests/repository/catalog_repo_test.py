"""Test module for CatalogRepo. These are integration tests and require that a
test db has been set up and its internal structure created."""
import unittest
from sqlalchemy.exc import SQLAlchemyError
from catalog_webapp_tests.db.test_engine import (TEST_ENGINE,
                                                 TEST_SESSION_FACTORY)
from catalog_webapp_tests.db.test_helper import DbTestHelper
from catalog_webapp.model.mapping_base import BASE
from catalog_webapp.model.catalog import Catalog
from catalog_webapp.model.user import User
from catalog_webapp.repository.catalog import CatalogRepo
from catalog_webapp.repository.user import UserRepo


# pylint: disable=missing-docstring
# pylint: disable=line-too-long


class CatalogRepoTest(unittest.TestCase):
    """Tester."""
    # pylint: disable=invalid-name

    _HELPER = DbTestHelper(TEST_ENGINE, BASE.metadata, TEST_SESSION_FACTORY)

    #
    # Set up and tear down methods.
    #
    @classmethod
    def tearDownClass(cls):
        """Reset database once all tests have run."""
        cls._HELPER.reset_database()

    def setUp(self):
        """Reset the database before each test is run"""
        CatalogRepoTest._HELPER.reset_database()

    def test_blank_database_has_no_catalogs(self):
        repo = CatalogRepo(TEST_SESSION_FACTORY)
        self.assertEqual([], repo.get_all())

    def test_cannot_add_unowned_catalog(self):
        repo = CatalogRepo(TEST_SESSION_FACTORY)
        catalog = Catalog(owner_id=None, name="catalog")
        with self.assertRaises(SQLAlchemyError):
            repo.add(catalog)

    def test_cannot_add_unamed_catalog(self):
        repo = CatalogRepo(TEST_SESSION_FACTORY)
        user_repo = UserRepo(TEST_SESSION_FACTORY)

        owner = User(username="bob", email="bob@bob")
        user_repo.add_user(owner)
        catalog = Catalog(owner_id=owner.id)
        with self.assertRaises(SQLAlchemyError):
            repo.add(catalog)

    def test_can_get_catalog_by_id_when_catalog_with_owner_and_name_added(self):
        repo = CatalogRepo(TEST_SESSION_FACTORY)
        user_repo = UserRepo(TEST_SESSION_FACTORY)

        owner = User(username="bob", email="bob@bob")
        user_repo.add_user(owner)
        catalog = Catalog(owner_id=owner.id, name="Bob's catalog.")
        repo.add(catalog)

        actual_catalog = repo.get_by_id(catalog.id)
        self.assertEqual(owner.id, actual_catalog.owner_id)
        self.assertEqual(catalog.name, actual_catalog.name)
        self.assertIsNone(actual_catalog.description)
        self.assertIsNotNone(actual_catalog.created_at_utc)

    def test_cannot_add_two_catalogs_with_same_name_and_owner(self):
        repo = CatalogRepo(TEST_SESSION_FACTORY)
        user_repo = UserRepo(TEST_SESSION_FACTORY)

        owner = User(username="bob", email="bob@bob")
        user_repo.add_user(owner)
        catalog = Catalog(owner_id=owner.id, name="A")
        repo.add(catalog)
        catalog = Catalog(owner_id=owner.id, name="A")
        with self.assertRaises(SQLAlchemyError):
            repo.add(catalog)

    def test_can_add_two_catalogs_with_same_name_and_different_owner(self):
        repo = CatalogRepo(TEST_SESSION_FACTORY)
        user_repo = UserRepo(TEST_SESSION_FACTORY)

        bob = User(username="bob", email="bob@bob")
        user_repo.add_user(bob)
        tony = User(username="tony", email="tony@tony")
        user_repo.add_user(tony)

        expected_catalogs = []
        catalog = Catalog(owner_id=bob.id, name="A")
        expected_catalogs.append(catalog)
        repo.add(catalog)
        catalog = Catalog(owner_id=tony.id, name="A")
        repo.add(catalog)
        expected_catalogs.append(catalog)

        self.assertEqual(sorted(expected_catalogs), sorted(repo.get_all()))

    def test_get_all_returns_all_when_catalog_contains_one_entry(self):
        repo = CatalogRepo(TEST_SESSION_FACTORY)
        user_repo = UserRepo(TEST_SESSION_FACTORY)

        owner = User(username="bob", email="bob@bob")
        user_repo.add_user(owner)
        catalog = Catalog(owner_id=owner.id, name="Bob's catalog.")
        repo.add(catalog)

        catalogs = repo.get_all()
        self.assertEqual(1, len(catalogs))
        self.assertEqual(owner.id, catalogs[0].owner_id)
        self.assertEqual(catalog.name, catalogs[0].name)
        self.assertIsNone(catalogs[0].description)
        self.assertIsNotNone(catalogs[0].created_at_utc)

    def test_get_all_returns_all_when_catalog_contains_more_than_one_entry(self):
        repo = CatalogRepo(TEST_SESSION_FACTORY)
        user_repo = UserRepo(TEST_SESSION_FACTORY)

        owner = User(username="bob", email="bob@bob")
        user_repo.add_user(owner)
        expected_catalogs = []
        expected_catalogs.append(Catalog(owner_id=owner.id, name="A"))
        expected_catalogs.append(Catalog(owner_id=owner.id, name="B"))
        expected_catalogs.append(Catalog(owner_id=owner.id, name="C"))

        for catalog in expected_catalogs:
            repo.add(catalog)

        actual_catalogs = repo.get_all()
        self.assertEqual(sorted(expected_catalogs), sorted(actual_catalogs))
