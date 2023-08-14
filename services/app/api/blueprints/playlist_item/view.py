from flasgger import swag_from
from flask import Blueprint, request

from http import HTTPStatus

playlist_items = Blueprint("playlist_items", __name__)


@swag_from("./docs/add.yml", endpoint="playlist_items.add", methods=["POST"])
@playlist_items.route("/playlist_item", methods=["POST"])
def add():
    return {'success':'created playlist'}, HTTPStatus.CREATED


@swag_from("./docs/update.yml", endpoint="playlist_items.update", methods=["PUT"])
@playlist_items.route("/playlist_item", methods=["PUT"])
def update():
    return {'success':'created playlist'}, HTTPStatus.CREATED


@swag_from("./docs/delete.yml", endpoint="playlist_items.delete", methods=["DELETE"])
@playlist_items.route("/playlist_item", methods=["DELETE"])
def delete():
    return {'success':'created playlist'}, HTTPStatus.CREATED


@swag_from("./docs/get.yml", endpoint="playlist_items.get", methods=["GET"])
@playlist_items.route("/playlist_item", methods=["GET"])
def get():
    return {'success':'created playlist'}, HTTPStatus.CREATED


@playlist_items.route("/", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add_many.yml", endpoint="playlist_items.add_many", methods=["POST"])
def add_many():
    return {'success':'created playlist'}, HTTPStatus.CREATED


@swag_from(
    "./docs/playlist_items.yml",
    endpoint="playlist_items.list_all_playlist_items",
    methods=["GET"],
)
@playlist_items.route("/", methods=["GET"])
def list_all_playlist_items():
    return {'success':'created playlist'}, HTTPStatus.CREATED


@swag_from("./docs/playlist_videos.yml", endpoint="playlist_items.video", methods=["GET"])
@playlist_items.route("/playlist_item/video", methods=["GET"])
def video():
    return {'success':'created playlist'}, HTTPStatus.CREATED
