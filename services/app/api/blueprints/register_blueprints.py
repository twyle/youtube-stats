"""This module registers the application blueprints.

Example:
    To register the blueprints:
        register_blueprints(app)

@Author: Lyle Okoth
@Date: 28/06/2023
@Portfolio: https://lyleokoth.oryks-sytem.com
"""

from flask import Flask

from .admin.view import admin
from .auth.view import auth
from .channel.view import channels
from .comment.view import comments
from ..blueprints.playlist.view import playlists
from .video.view import videos


def register_blueprints(app: Flask) -> None:
    """Register the application blueprints.

    Parameters
    ----------
    app: flask.Flask
        The Flask app instance.
    """
    app.register_blueprint(videos, url_prefix="/api/v1/videos")
    app.register_blueprint(auth, url_prefix="/api/v1/auth")
    app.register_blueprint(channels, url_prefix="/api/v1/channels")
    app.register_blueprint(admin, url_prefix="/api/v1/admin")
    app.register_blueprint(playlists, url_prefix="/api/v1/playlists")
    app.register_blueprint(comments, url_prefix="/api/v1/comments")
