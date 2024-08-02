#!/usr/bin/env python3
"""
Flask app with Babel for language support,
including user-based locale and timezone settings.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext as _
import pytz
from pytz import UnknownTimeZoneError


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config:
    """Configuration for Flask app."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

def get_user():
    """Get the logged-in user from the mock user table."""
    user_id = request.args.get('login_as')
    if user_id:
        try:
            user_id = int(user_id)
            return users.get(user_id)
        except ValueError:
            pass
    return None

@app.before_request
def before_request():
    """
    et the user as a global on flask.g
    before each request.
    """
    g.user = get_user()

@babel.localeselector
def get_locale():
    """
    Determine the best match with supported languages.

    The order of priority is:
    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request headers
    4. Default locale
    """
    url_locale = request.args.get('locale')
    if url_locale in app.config['LANGUAGES']:
        return url_locale

   
    user = g.user
    if user and user.get('locale') in app.config['LANGUAGES']:
        return user.get('locale')

    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    """
    Determine the best match for timezone.

    The order of priority is:
    1. Timezone from URL parameters
    2. Timezone from user settings
    3. Default to UTC
    """

    url_timezone = request.args.get('timezone')
    if url_timezone:
        try:
            pytz.timezone(url_timezone)
            return url_timezone
        except UnknownTimeZoneError:
            pass

    user = g.user
    if user and user.get('timezone'):
        try:
            pytz.timezone(user.get('timezone'))
            return user.get('timezone')
        except UnknownTimeZoneError:
            pass

    # Default to UTC
    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route("/", strict_slashes=False)
def index():
    """Render the index page."""
    return render_template('7-index.html')

if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
