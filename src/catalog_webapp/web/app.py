"""The web application entry point for the catalog web application"""
from flask import Flask


APP = Flask(__name__)


@APP.route("/")
def index():
    """Main page."""
    return "This is the temporary index page for the catalog application."
