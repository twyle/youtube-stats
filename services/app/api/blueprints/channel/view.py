from flasgger import swag_from
from flask import Blueprint
from flask_jwt_extended import jwt_required

from http import HTTPStatus

#from ..decorators import admin_token_required

channels = Blueprint("channels", __name__)


@channels.route("/channel", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add.yml", endpoint="channels.add", methods=["POST"])
def add():
    return {'success':'channel'}, HTTPStatus.CREATED


@channels.route("/channel", methods=["PUT"])
# @admin_token_required
@swag_from("./docs/update.yml", endpoint="channels.update", methods=["PUT"])
def update():
    return {'success':'channel'}, HTTPStatus.CREATED


@channels.route("/channel", methods=["DELETE"])
# @admin_token_required
@swag_from("./docs/delete.yml", endpoint="channels.delete", methods=["DELETE"])
def delete():
    return {'success':'channel'}, HTTPStatus.CREATED


@channels.route("/channel", methods=["GET"])
# @admin_token_required
@swag_from("./docs/get.yml", endpoint="channels.get", methods=["GET"])
def get():
    return {'success':'channel'}, HTTPStatus.CREATED


@channels.route("/", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add_many.yml", endpoint="channels.add_many", methods=["POST"])
def add_many():
    return {'success':'channel'}, HTTPStatus.CREATED


@channels.route("/", methods=["GET"])
# @jwt_required()
@swag_from("./docs/channels.yml", endpoint="channels.list_all_channels", methods=["GET"])
def list_all_channels():
    return {'success':'channel'}, HTTPStatus.CREATED


@channels.route("/channel/videos", methods=["GET"])
# @jwt_required()
@swag_from("./docs/add.yml", endpoint="channels.channel_Channels", methods=["GET"])
def channel_videos():
    return {'success':'channel'}, HTTPStatus.CREATED


@channels.route("/channel/playlists", methods=["GET"])
# @jwt_required()
@swag_from("./docs/videos.yml", endpoint="channels.channel_playlists", methods=["GET"])
def channel_playlists():
    return {'success':'channel'}, HTTPStatus.CREATED


@channels.route("/channel/comments", methods=["GET"])
# @jwt_required()
@swag_from("./docs/add.yml", endpoint="channels.channel_comments", methods=["GET"])
def channel_comments():
    return {'success':'channel'}, HTTPStatus.CREATED
