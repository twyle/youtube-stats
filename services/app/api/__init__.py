"""This is the application entry point.

This script:
1. Registers the error handlers.
2. Sets the configuration.
3. Registers the blueprints
4. Registers the extensions
"""
from http import HTTPStatus

from flask import Flask, jsonify, request
from .helpers.hooks import (
    get_exception,
    get_response,
    log_get_request,
    log_post_request,
)

# from .helpers.error_handlers import register_error_handlers
from .config.set_config import set_configuration
from .config.logger_config import app_logger
from .blueprints.register_blueprints import register_blueprints
from .extensions.register_extensions import register_extensions


def create_app(flask_env: str = "development") -> Flask:
    """Create the flask app instance.

    Parameters
    ----------
    flask_env: str
        The Environment under which this application will run. can be 'Development', 'Test', 'Staging' or 'Production'.

    Returns
    -------
    app: flask.Flask
        The Flask app instance.
    """
    app = Flask(__name__)

    set_configuration(app, flask_env=flask_env)
    # register_error_handlers(app)
    register_extensions(app)
    register_blueprints(app)

    @app.route("/", methods=["GET"])
    def health_check():
        """Check whether the application is up and running."""
        return jsonify({"success": "Hello from the stats API."}), HTTPStatus.OK
    
    @app.before_first_request
    def application_startup():
        """Log the beginning of the application."""
        app_logger.info('Web app is up!')

    @app.before_request
    def log_request():
        """Log the data held in the request"""
        if request.method in ['POST', 'PUT']:
            log_post_request()
        elif request.method in ['GET', 'DELETE']:
            log_get_request()

    @app.after_request
    def log_response(response):
        try:
            get_response(response)
        except Exception:
            pass
        finally:
            return response

    @app.teardown_request
    def log_exception(exc):
        get_exception(exc)

    app.shell_context_processor({"app": app})

    return app
