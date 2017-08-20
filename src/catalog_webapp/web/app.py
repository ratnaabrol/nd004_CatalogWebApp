"""The web application entry point for the catalog web application"""
import random
import json
import string
from flask import (Flask, render_template, request, redirect, url_for, flash,
                   session, make_response)
from oauth2client import client, crypt
from catalog_webapp.db.default_engine import SESSION_FACTORY
from catalog_webapp.model.auth_provider import AuthProvider
from catalog_webapp.model.user import User
from catalog_webapp.repository.user import UserRepo

APP = Flask(__name__)
_USER_REPO = UserRepo(SESSION_FACTORY)
WEBAPP_CLIENT_ID = \
    "103412510527-l53qc3670gg7tved63dvqer4c0ldr4go.apps.googleusercontent.com"


@APP.route("/")
def index():
    """Main page."""
    msg = "This is the temporary index page for the catalog application."
    if "user_email" in session:
        msg = "You are logged in as {}".format(session["user_email"]) + msg
    return render_template("index.html")


@APP.route("/register", methods=["GET"])
def register():
    """Register user"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    session['state'] = state
    return render_template("register.html", STATE=state)


@APP.route("/logout", methods=["GET", "POST"])
def logout():
    """Logout user"""
    session.pop("user_email", None)
    return redirect(url_for("index"))


@APP.route("/googleTokenRegister", methods=["POST"])
def google_register():
    """Register a user using a google provider."""

    # protect against CSFR
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    token = request.values["idtoken"]
    try:
        idinfo = client.verify_id_token(token, WEBAPP_CLIENT_ID)
        if idinfo["iss"] not in ["accounts.google.com",
                                 "https://accounts.google.com"]:
            raise crypt.AppIdentityError("Wrong issuer.")

        username = idinfo["sub"]
        if not _USER_REPO.exists_by_username(username, AuthProvider.google):
            # add user
            user = User(username=username,
                        provider=AuthProvider.google,
                        email=idinfo["email"])
            _USER_REPO.add_user(user)
            print("Added user")
            session["user_email"] = user.email
            return redirect(url_for("index"))

        print("Cannot register already registered user.")
        return "", 409  # conflict
    except crypt.AppIdentityError:
        # redirect to error page
        print("Invalid request to register a user.")
        flash("Invalid request to register a user.")
        return redirect(url_for("register"))
