from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from http import HTTPStatus


auth = Blueprint("auth", __name__)


@swag_from("./docs/register.yml", endpoint="auth.register_client", methods=["POST"])
@auth.route("/register", methods=["POST"])
def register_client():
    return {'success': 'registered'}, HTTPStatus.CREATED


@auth.route("/get", methods=["GET"])
# @jwt_required()
@swag_from("./docs/get.yml", endpoint="auth.get_client", methods=["GET"])
def get_client():
    return {'success': 'registered'}, HTTPStatus.CREATED


@auth.route("/update", methods=["PUT"])
# @jwt_required()
@swag_from("./docs/update.yml", endpoint="auth.update_client", methods=["PUT"])
def update_client():
    return {'success': 'registered'}, HTTPStatus.CREATED


@auth.route("/delete", methods=["DELETE"])
# @admin_token_required
@swag_from("./docs/delete.yml", endpoint="auth.delete_client", methods=["DELETE"])
def delete_client():
    return {'success': 'registered'}, HTTPStatus.CREATED


@auth.route("/users", methods=["GET"])
# @admin_token_required
@swag_from("./docs/users.yml", endpoint="auth.list_all", methods=["GET"])
def list_all():
    return {'success': 'registered'}, HTTPStatus.CREATED


@swag_from("./docs/activate.yml", endpoint="auth.activate_account", methods=["GET"])
@auth.route("/activate", methods=["GET"])
def activate_account():
    """Activate User account."""
    return {'success': 'registered'}, HTTPStatus.CREATED


@swag_from("./docs/login.yml", endpoint="auth.login_client", methods=["POST"])
@auth.route("/login", methods=["POST"])
def login_client():
    """Login a registered, confirmed client."""
    return {'success': 'registered'}, HTTPStatus.CREATED


@swag_from(
    "./docs/password_reset.yml",
    endpoint="auth.request_client_password_reset",
    methods=["GET"],
)
@auth.route("/request_password_reset", methods=["GET"])
def request_client_password_rest():
    """Request a client password reset."""
    return {'success': 'registered'}, HTTPStatus.CREATED


@swag_from("./docs/reset_password.yml", endpoint="auth.reset_password", methods=["POST"])
@auth.route("/reset_password", methods=["POST"])
def reset_client_password():
    """Reset a client password."""
    return {'success': 'registered'}, HTTPStatus.CREATED


@auth.route("/refresh_token", methods=["POST"])
@swag_from("./docs/refresh_token.yml", endpoint="auth.refresh_token", methods=["POST"])
def refresh_token():
    """Refresh an expired token."""
    return {'success': 'registered'}, HTTPStatus.CREATED
