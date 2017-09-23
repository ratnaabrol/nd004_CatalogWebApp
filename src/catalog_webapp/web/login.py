"""Login helpers."""

from functools import wraps
from flask import session, request, redirect, url_for


def login_required(fnc):
    """Decorator, ensuring that route is only accessable if a user is logged
       in."""
    @wraps(fnc)
    def decorated_function(*args, **kwargs):  # pylint: disable=missing-docstring
        if "user_email" not in session:
            session["next"] = request.url
            return redirect(url_for('login'))
        return fnc(*args, **kwargs)
    return decorated_function


def admin_required(fnc):
    """Decorator, ensuring that route is only accessable if a user is an
       admin."""
    @wraps(fnc)
    def decorated_function(*args, **kwargs):  # pylint: disable=missing-docstring
        if "user_admin" not in session or not session["user_admin"]:
            return redirect(url_for('index'))
        return fnc(*args, **kwargs)
    return decorated_function
