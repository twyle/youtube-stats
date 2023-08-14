from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from http import HTTPStatus


#from ..decorators import admin_token_required


comment_authors = Blueprint("comment_authors", __name__)


@comment_authors.route("/register", methods=["POST"])
# @admin_token_required
@swag_from(
    "./docs/register.yml",
    endpoint="comment_authors.register_comment_author",
    methods=["POST"],
)
def register_comment_author():
    return {'author':'created'}, HTTPStatus.CREATED


@comment_authors.route("/get", methods=["GET"])
# @jwt_required()
@swag_from("./docs/get.yml", endpoint="comment_authors.get_comment_author", methods=["GET"])
def get_comment_author():
    return {'author':'created'}, HTTPStatus.CREATED


@comment_authors.route("/update", methods=["PUT"])
# @admin_token_required
@swag_from(
    "./docs/update.yml",
    endpoint="comment_authors.update_comment_author",
    methods=["PUT"],
)
def update_comment_author():
    return {'author':'created'}, HTTPStatus.CREATED


@comment_authors.route("/delete", methods=["DELETE"])
# @admin_token_required
@swag_from(
    "./docs/delete.yml",
    endpoint="comment_authors.delete_comment_author",
    methods=["DELETE"],
)
def delete_comment_author():
    return {'author':'created'}, HTTPStatus.CREATED


@comment_authors.route("/", methods=["GET"])
# @jwt_required()
@swag_from("./docs/users.yml", endpoint="comment_authors.list_all", methods=["GET"])
def list_all():
    return {'author':'created'}, HTTPStatus.CREATED
