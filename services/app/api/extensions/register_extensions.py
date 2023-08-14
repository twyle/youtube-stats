"""This module resgisters the application extensions.

Example:
    To register the extensions:
        register_extensions(app)

@Author: Lyle Okoth
@Date: 28/06/2023
@Portfolio: https://lyleokoth.oryks-sytem.com
"""
from flasgger import LazyJSONEncoder
from flask import Flask

from .extensions import bcrypt, jwt, swagger


def register_extensions(app: Flask) -> None:
    """Register the application extensions.

    Parameters
    ----------
    app: flask.Flask
        The Flask app instance.
    """
    app.json_encoder = LazyJSONEncoder
    swagger.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
