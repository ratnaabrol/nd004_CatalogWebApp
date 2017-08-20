"""Test module for UserRepo. These are integration tests and require that a
test db has been set up and its internal structure created."""
import unittest
from catalog_webapp_tests.db.test_engine import (TEST_ENGINE,
                                                 TEST_SESSION_FACTORY)
from catalog_webapp_tests.db.test_helper import DbTestHelper
from catalog_webapp.repository.user import UserRepo
from catalog_webapp.model.mapping_base import BASE
from catalog_webapp.model.user import User

# pylint: disable=missing-docstring


class UserRepoTest(unittest.TestCase):
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
        UserRepoTest._HELPER.reset_database()

    def test_exists_by_username_returns_false_when_no_user_exists(self):
        repo = UserRepo(TEST_SESSION_FACTORY)
        self.assertFalse(repo.exists_by_username("badusername"))

    def test_exists_by_username_returns_true_when_user_exists(self):
        repo = UserRepo(TEST_SESSION_FACTORY)
        repo.add_user(User(username="goodusername", email="good@somewhere"))
        self.assertTrue(repo.exists_by_username("goodusername"))
