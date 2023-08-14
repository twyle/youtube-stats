from flasgger import swag_from
from flask import Blueprint
from http import HTTPStatus


admin = Blueprint("admin", __name__)


@swag_from("./docs/register.yml", endpoint="admin.register", methods=["POST"])
@admin.route("/register", methods=["POST"])
def register():
    return {'Succes':'registered'}, HTTPStatus.CREATED


@swag_from("./docs/login.yml", endpoint="admin.login_client", methods=["POST"])
@admin.route("/login", methods=["POST"])
def login_client():
    """Login a registered, confirmed client."""
    return {'Succes':'registered'}, HTTPStatus.CREATED


@admin.route("/get", methods=["GET"])
# @admin_token_required
@swag_from("./docs/get.yml", endpoint="admin.get", methods=["GET"])
def get():
    return {'Succes':'registered'}, HTTPStatus.CREATED


@admin.route("/update", methods=["PUT"])
# @admin_token_required
@swag_from("./docs/update.yml", endpoint="admin.update", methods=["PUT"])
def update():
    return {'Succes':'registered'}, HTTPStatus.CREATED


@admin.route("/delete", methods=["DELETE"])
# @admin_token_required
@swag_from("./docs/delete.yml", endpoint="admin.delete", methods=["DELETE"])
def delete():
    return {'Succes':'registered'}, HTTPStatus.CREATED


@admin.route("/list_all", methods=["GET"])
# @admin_token_required
@swag_from("./docs/admins.yml", endpoint="admin.list_all", methods=["GET"])
def list_all():
    return {'Succes':'registered'}, HTTPStatus.CREATED