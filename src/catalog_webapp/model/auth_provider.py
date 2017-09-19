"""The set of auth providers supported by this application."""
from enum import Enum


class AuthProvider(Enum):
    """Authorization provider enumeration."""
    local = 0
    google = 1

    def __str__(self):
        return self.name.capitalize()
