from flasgger import swag_from
from flask import Blueprint, request
from http import HTTPStatus

comments = Blueprint("comments", __name__)


@swag_from("./docs/add.yml", endpoint="comments.add", methods=["POST"])
@comments.route("/comment", methods=["POST"])
def add():
    return {'comment': 'created'}, HTTPStatus.CREATED


@swag_from("./docs/update.yml", endpoint="comments.update", methods=["PUT"])
@comments.route("/comment", methods=["PUT"])
def update():
    return {'comment': 'created'}, HTTPStatus.CREATED


@swag_from("./docs/delete.yml", endpoint="comments.delete", methods=["DELETE"])
@comments.route("/comment", methods=["DELETE"])
def delete():
    return {'comment': 'created'}, HTTPStatus.CREATED


@swag_from("./docs/get.yml", endpoint="comments.get", methods=["GET"])
@comments.route("/comment", methods=["GET"])
def get():
    return {'comment': 'created'}, HTTPStatus.CREATED


@comments.route("/", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add_many.yml", endpoint="comments.add_many", methods=["POST"])
def add_many():
    return {'comment': 'created'}, HTTPStatus.CREATED


@swag_from("./docs/comments.yml", endpoint="comments.list_all_comments", methods=["GET"])
@comments.route("/", methods=["GET"])
def list_all_comments():
    return {'comment': 'created'}, HTTPStatus.CREATED


@swag_from("./docs/videos.yml", endpoint="comments.video_comments", methods=["GET"])
@comments.route("/video/", methods=["GET"])
def video_comments():
    return {'comment': 'created'}, HTTPStatus.CREATED


@swag_from("./docs/channels.yml", endpoint="channels.channel_channels", methods=["GET"])
@comments.route("/channel/", methods=["GET"])
def channel_channels():
    return {'comment': 'created'}, HTTPStatus.CREATED
