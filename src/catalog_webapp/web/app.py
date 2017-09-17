"""The web application entry point for the catalog web application."""
import random
import json
import string
from pkg_resources import resource_string
from flask import (Flask, render_template, request, redirect, url_for,
                   session, make_response)
from oauth2client import client
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
    """Display main page."""
    msg = "This is the temporary index page for the catalog application."
    if "user_email" in session:
        msg = "You are logged in as {}".format(session["user_email"]) + msg
    return render_template("index.html")


@APP.route("/register", methods=["GET"])
def register():
    """Display register user."""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    session['state'] = state
    return render_template("register.html", STATE=state)


@APP.route("/login", methods=["GET"])
def login():
    """Login user."""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    session['state'] = state
    return render_template("login.html", STATE=state)


@APP.route("/logout", methods=["GET", "POST"])
def logout():
    """Logout user."""
    session.pop("user_email", None)
    return redirect(url_for("index"))


@APP.route("/googleOneTimeCode/register", methods=["POST"])
def google_register():
    """Register a user using a google provider."""
    # protect against CSFR
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    one_time_code = request.values["code"]
    credentials = None
    try:
        # upgrade one-time code from client into oauth2 credentials
        secrets =\
            json.loads(resource_string(__name__,
                                       "client_secrets.json").decode("utf-8"))
        credentials =\
            client.credentials_from_code(WEBAPP_CLIENT_ID,
                                         secrets["web"]["client_secret"],
                                         "",
                                         one_time_code)
    except client.FlowExchangeError:
        response =\
            make_response(json.dumps('Failed to upgrade google auth code.'),
                          401)
        response.headers['Content-Type'] = 'application/json'
        return response

    username = credentials.id_token["sub"]
    if not _USER_REPO.exists_by_username(username, AuthProvider.google):
        # add user
        user = User(username=username,
                    provider=AuthProvider.google,
                    email=credentials.id_token["email"])
        _USER_REPO.add_user(user)
        print("Added user")
        return "", 200

    print("User already registered.")
    response =\
        make_response(json.dumps('User already registered.'), 409)
    response.headers['Content-Type'] = 'application/json'
    return response


@APP.route("/googleOneTimeCode/login", methods=["POST"])
def google_login():
    """Log in using google oauth2."""
    # protect against CSFR
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    one_time_code = request.values["code"]
    credentials = None
    try:
        # upgrade one-time code from client into oauth2 credentials
        secrets =\
            json.loads(resource_string(__name__,
                                       "client_secrets.json").decode("utf-8"))
        credentials =\
            client.credentials_from_code(WEBAPP_CLIENT_ID,
                                         secrets["web"]["client_secret"],
                                         "",
                                         one_time_code)
    except client.FlowExchangeError:
        response =\
            make_response(json.dumps('Failed to upgrade google auth code.'),
                          401)
        response.headers['Content-Type'] = 'application/json'
        return response

    username = credentials.id_token["sub"]
    if _USER_REPO.exists_by_username(username, AuthProvider.google):
        # user logged in
        print("User logged in.")
        session["user_email"] = credentials.id_token["email"]
        return "", 200

    print("Unknown user.")
    response =\
        make_response(json.dumps('Unknown user.'), 403)
    response.headers['Content-Type'] = 'application/json'
    return response
