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

    def test_get_all_with_no_users_returns_an_empty_list(self):
        repo = UserRepo(TEST_SESSION_FACTORY)
        users = repo.get_all_users()
        self.assertEqual([], users)

    def test_get_all_with_one_user_returns_that_user(self):
        repo = UserRepo(TEST_SESSION_FACTORY)
        u = User(username="goodusername", email="good@somewhere")
        repo.add_user(u)
        users = repo.get_all_users()
        self.assertEqual(1, len(users))
        self.assertEqual(u, users[0])

    def test_get_all_with_more_than_one_user_returns_all_users(self):
        repo = UserRepo(TEST_SESSION_FACTORY)
        u1 = User(username="goodusername", email="good@somewhere")
        u2 = User(username="agoodusername", email="agood@somewhere")
        u3 = User(username="bgoodusername", email="bgood@somewhere")
        repo.add_user(u1)
        repo.add_user(u2)
        repo.add_user(u3)
        users = repo.get_all_users()
        expected = [u1, u2, u3]
        self.assertEqual(len(expected), len(users))
        self.assertListEqual(expected, users)
