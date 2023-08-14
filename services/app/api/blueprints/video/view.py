from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from http import HTTPStatus

videos = Blueprint("videos", __name__)


@videos.route("/video", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add.yml", endpoint="videos.add", methods=["POST"])
def add():
    controller = AddVideoControllerFactory()
    return flow(controller)


@videos.route("/", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add_many.yml", endpoint="videos.add_many", methods=["POST"])
def add_many():
    return {'video':'succes'}, HTTPStatus.CREATED


@videos.route("/video", methods=["GET"])
# @jwt_required()
@swag_from("./docs/get.yml", endpoint="videos.get", methods=["GET"])
def get():
    return {'video':'succes'}, HTTPStatus.CREATED


@videos.route("/video", methods=["PUT"])
# @admin_token_required
@swag_from("./docs/update.yml", endpoint="videos.update", methods=["PUT"])
def update():
    return {'video':'succes'}, HTTPStatus.CREATED


@videos.route("/video", methods=["DELETE"])
# @admin_token_required
@swag_from("./docs/delete.yml", endpoint="videos.delete", methods=["DELETE"])
def delete():
    return {'video':'succes'}, HTTPStatus.CREATED


@videos.route("/", methods=["GET"])
# @jwt_required()
@swag_from("./docs/videos.yml", endpoint="videos.list_all", methods=["GET"])
def list_all():
    return {'video':'succes'}, HTTPStatus.CREATED


@videos.route("/advanced", methods=["POST"])
# @jwt_required()
@swag_from("./docs/advanced_search.yml", endpoint="videos.advanced_search", methods=["POST"])
def advanced_search():
    return {'video':'succes'}, HTTPStatus.CREATED


@videos.route("/video/comments", methods=["GET"])
# @jwt_required()
@swag_from("./docs/comments.yml", endpoint="videos.get_video_comments", methods=["GET"])
def get_video_comments():
    """Get the comments for a particular video."""
    return {'video':'succes'}, HTTPStatus.CREATED
