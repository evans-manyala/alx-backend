#!/usr/bin/env python3
"""
Basic Flask app with a single route and a template.

This app serves a single page with a title and header.
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """
    Render the index page.
    
    Returns:
        str: Rendered HTML content of the index page.
    """
    return render_template('0-index.html')

if __name__ == '__main__':
    app.run(debug=True)
