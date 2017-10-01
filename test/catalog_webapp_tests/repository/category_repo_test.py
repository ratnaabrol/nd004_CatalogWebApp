"""Test module for CategoryRepo. These are integration tests and require that a
test db has been set up and its internal structure created."""
import unittest
from sqlalchemy.exc import SQLAlchemyError
from catalog_webapp_tests.db.test_engine import (TEST_ENGINE,
                                                 TEST_SESSION_FACTORY)
from catalog_webapp_tests.db.test_helper import DbTestHelper
from catalog_webapp.model.mapping_base import BASE
from catalog_webapp.model.catalog import Catalog
from catalog_webapp.model.category import Category
from catalog_webapp.model.user import User
from catalog_webapp.repository.catalog import CatalogRepo
from catalog_webapp.repository.category import CategoryRepo
from catalog_webapp.repository.user import UserRepo


# pylint: disable=missing-docstring
# pylint: disable=line-too-long


class CategoryRepoTest(unittest.TestCase):
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
        CategoryRepoTest._HELPER.reset_database()

        # add a test owners
        user_repo = UserRepo(TEST_SESSION_FACTORY)
        self._test_owner = User(username="bob", email="bob@bob")
        self._test_owner2 = User(username="tony", email="tony@tony")
        user_repo.add_user(self._test_owner)
        user_repo.add_user(self._test_owner2)

        # add a test catalogs
        catalogRepo = CatalogRepo(TEST_SESSION_FACTORY)
        self._test_catalog = Catalog(owner_id=self._test_owner.id,
                                     name="catalog")
        self._test_catalog2 = Catalog(owner_id=self._test_owner2.id,
                                      name="catalog two")
        catalogRepo.add(self._test_catalog)
        catalogRepo.add(self._test_catalog2)

    def test_blank_database_has_no_categories(self):
        repo = CategoryRepo(TEST_SESSION_FACTORY)
        self.assertEqual([], repo.get_all())

    def test_cannot_add_unowned_category(self):
        repo = CategoryRepo(TEST_SESSION_FACTORY)
        category = Category(owner_id=None, catalog_id=self._test_catalog.id, name="category")
        with self.assertRaises(SQLAlchemyError):
            repo.add(category)

    def test_cannot_add_unamed_category(self):
        repo = CategoryRepo(TEST_SESSION_FACTORY)
        category = Category(owner_id=self._test_owner.id, catalog_id=self._test_catalog.id, name=None)
        with self.assertRaises(SQLAlchemyError):
            repo.add(category)

    def test_can_get_category_by_id_when_category_with_owner_and_name_added(self):
        repo = CategoryRepo(TEST_SESSION_FACTORY)
        category = Category(owner_id=self._test_owner.id,
                            catalog_id=self._test_catalog.id,
                            name="Bob's category.")
        repo.add(category)

        actual_category = repo.get_by_id(category.id)
        self.assertEqual(category, actual_category)

    def test_cannot_add_two_categories_with_same_name_and_catalog(self):
        repo = CategoryRepo(TEST_SESSION_FACTORY)

        category = Category(owner_id=self._test_owner.id,
                            catalog_id=self._test_catalog.id,
                            name="Bob's category.")
        repo.add(category)
        category = Category(owner_id=self._test_owner2.id,
                            catalog_id=self._test_catalog.id,
                            name="Bob's category.")
        with self.assertRaises(SQLAlchemyError):
            repo.add(category)

    def test_can_add_two_categories_with_same_name_and_different_catalogs(self):
        repo = CategoryRepo(TEST_SESSION_FACTORY)

        expected_categories = []
        category = Category(owner_id=self._test_owner.id,
                            catalog_id=self._test_catalog.id,
                            name="Bob's category.")
        expected_categories.append(category)
        repo.add(category)
        category = Category(owner_id=self._test_owner.id,
                            catalog_id=self._test_catalog2.id,
                            name="Bob's category.")
        repo.add(category)
        expected_categories.append(category)

        self.assertEqual(sorted(expected_categories), sorted(repo.get_all()))

    def test_get_all_returns_all_when_categories_contains_one_entry(self):
        repo = CategoryRepo(TEST_SESSION_FACTORY)

        category = Category(owner_id=self._test_owner.id,
                            catalog_id=self._test_catalog2.id,
                            name="Bob's category.")
        repo.add(category)

        actual_categories = repo.get_all()
        self.assertEqual(1, len(actual_categories))
        self.assertEqual(category, actual_categories[0])

    def test_get_all_returns_all_when_categoryies_contains_more_than_one_entry(self):
        repo = CategoryRepo(TEST_SESSION_FACTORY)

        expected_categories = []
        expected_categories.append(Category(owner_id=self._test_owner.id,
                                            catalog_id=self._test_catalog2.id,
                                            name="A"))
        expected_categories.append(Category(owner_id=self._test_owner.id,
                                            catalog_id=self._test_catalog2.id,
                                            name="B"))
        expected_categories.append(Category(owner_id=self._test_owner.id,
                                            catalog_id=self._test_catalog2.id,
                                            name="C"))

        for category in expected_categories:
            repo.add(category)

        actual_categories = repo.get_all()
        self.assertEqual(sorted(expected_categories), sorted(actual_categories))
