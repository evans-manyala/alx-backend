#!/usr/bin/env python3
"""
Basic Flask app with Babel for language support and user login simulation.

This app serves a single page with a title and header, supporting multiple
languages and simulating user login.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext as _


class Config:
    """Configuration for Flask app."""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> dict:
    """
    Get a user dictionary based on the login_as URL parameter.

    Returns:
        dict: The user dictionary if found, otherwise None.
    """
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """
    Execute before all other functions. Sets the user as a global variable.
    """
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Determine the best match with supported languages.

    Check if a 'locale' parameter is present in the request arguments
    and if it is a supported locale. Otherwise, use the request's
    accept languages to find the best match.

    Returns:
        str: The best match language.
    """
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale
    if g.user and g.user.get("locale") in app.config["LANGUAGES"]:
        return g.user["locale"]
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/", strict_slashes=False)
def index() -> str:
    """
    Render the index page.

    Returns:
        str: Rendered HTML content of the index page.
    """
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run(debug=True)
