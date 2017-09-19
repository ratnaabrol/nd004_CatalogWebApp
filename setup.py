"""Project build script. This uses setuptools to drive the build."""

import unittest
from setuptools import setup, find_packages

# configure test discovery
TEST_DIR = "test"
TEST_PATTERN = "*_test.py"


def test_suite():
    '''Creates test suite using the unittest module's discovery algorithm.'''
    loader = unittest.TestLoader()
    suite = loader.discover(TEST_DIR, TEST_PATTERN)
    return suite


setup(
    name="catalog_webapp",
    version="1.0.0",
    namespace_packages=["catalog_webapp"],
    python_requires=">=3",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["flask==0.12.2",
                      "oauth2client==4.1.2",
                      "sqlalchemy==1.1.13"],
    test_suite="setup.test_suite"
)
