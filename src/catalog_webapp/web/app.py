"""The web application entry point for the catalog web application"""
from flask import Flask, render_template


APP = Flask(__name__)


@APP.route("/")
def index():
    """Main page."""
    return "This is the temporary index page for the catalog application."

@APP.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    return render_template("register.html")
