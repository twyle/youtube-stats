from flasgger import swag_from
from flask import Blueprint, request

from http import HTTPStatus

playlists = Blueprint("playlists", __name__)


@swag_from("./docs/add.yml", endpoint="playlists.add", methods=["POST"])
@playlists.route("/playlist", methods=["POST"])
def add():
    return {'success':'playlist'}, HTTPStatus.CREATED


@swag_from("./docs/update.yml", endpoint="playlists.update", methods=["PUT"])
@playlists.route("/playlist", methods=["PUT"])
def update():
    return {'success':'playlist'}, HTTPStatus.CREATED


@swag_from("./docs/delete.yml", endpoint="playlists.delete", methods=["DELETE"])
@playlists.route("/playlist", methods=["DELETE"])
def delete():
    return {'success':'playlist'}, HTTPStatus.CREATED


@swag_from("./docs/get.yml", endpoint="playlists.get", methods=["GET"])
@playlists.route("/playlist", methods=["GET"])
def get():
    return {'success':'playlist'}, HTTPStatus.CREATED


@playlists.route("/", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add_many.yml", endpoint="playlists.add_many", methods=["POST"])
def add_many():
    return {'success':'playlist'}, HTTPStatus.CREATED


@swag_from("./docs/playlists.yml", endpoint="playlists.list_all_playlists", methods=["GET"])
@playlists.route("/", methods=["GET"])
def list_all_playlists():
    return {'success':'playlist'}, HTTPStatus.CREATED


@swag_from("./docs/channel.yml", endpoint="playlists.channel_playlists", methods=["GET"])
@playlists.route("/channel/", methods=["GET"])
def channel_playlists():
    return {'success':'playlist'}, HTTPStatus.CREATED


@swag_from("./docs/playlist_videos.yml", endpoint="playlists.videos", methods=["GET"])
@playlists.route("/playlist/videos", methods=["GET"])
def videos():
    return {'success':'playlist'}, HTTPStatus.CREATED
