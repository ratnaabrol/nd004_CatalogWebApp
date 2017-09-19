"""Login helpers."""

from functools import wraps
from flask import session, request, redirect, url_for


def login_required(f):
    """Decorator, ensuring that route is only accessable if a user is logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_email" not in session:
            session["next"] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
