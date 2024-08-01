#!/usr/bin/env python3
"""
Basic Flask app with Babel for language support.

This app serves a single page with a title and header,
supporting multiple languages.
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration for Flask app."""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale():
    """
    Determine the best match with supported languages.

    Uses the request's accept languages to find the best match.

    Returns:
        str: The best match language.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/", strict_slashes=False)
def index() -> str:
    """
    Render the index page.

    Returns:
        str: Rendered HTML content of the index page.
    """
    return render_template(
        "4-index.html", title=_("home_title"), header=_("home_header")
    )


if __name__ == "__main__":
    app.run(debug=True)
