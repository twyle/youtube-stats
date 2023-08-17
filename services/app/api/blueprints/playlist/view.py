from flasgger import swag_from
from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..database.crud.playlist import (
    create_playlist, create_many, get_playlist, delete_playlist, get_playlists
)
from ..database.schema.playlist import (
    Playlist as PlaylistSchema, Playlists as PlaylistsSchema, GetPlaylist, GetPlaylists
)
from ..database.database import get_db
from http import HTTPStatus
from pydantic import ValidationError
from flask import request

#from ..decorators import admin_token_required

playlists = Blueprint("playlists", __name__)


@swag_from("./docs/add.yml", endpoint="playlists.add", methods=["POST"])
@playlists.route("/playlist", methods=["POST"])
def add():
    try:
        playlist_data = PlaylistSchema(**request.json)
    except ValidationError:
        return {'Error': 'Invalid playlist data!'}, HTTPStatus.BAD_REQUEST
    playlist = get_playlist(session=get_db, playlist_data=playlist_data)
    if playlist:
        return {'Error': f'playlist with id {playlist_data.playlist_id} already exists'}, HTTPStatus.CONFLICT
    playlist = create_playlist(playlist_data=playlist_data, session=get_db)
    resp = PlaylistSchema(
        playlist_description=playlist.playlist_description,
        playlist_id=playlist.playlist_id,
        playlist_title=playlist.playlist_title,
        playlist_thumbnail=playlist.playlist_thumbnail,
        published_at=playlist.published_at,
        privacy_status=playlist.privacy_status,
        videos_count=playlist.videos_count,
        channel_id=playlist.channel_id
    )
    
    return resp.model_dump_json(indent=4), HTTPStatus.CREATED


@swag_from("./docs/update.yml", endpoint="playlists.update", methods=["PUT"])
@playlists.route("/playlist", methods=["PUT"])
def update():
    return {'success':'playlist'}, HTTPStatus.CREATED


@swag_from("./docs/delete.yml", endpoint="playlists.delete", methods=["DELETE"])
@playlists.route("/playlist", methods=["DELETE"])
def delete():
    try:
        playlist_data = GetPlaylist(playlist_id=request.args.get('playlist_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the playlist id.'}, HTTPStatus.BAD_REQUEST
    playlist = get_playlist(session=get_db, playlist_data=playlist_data)
    if not playlist:
        return {'Error': f'playlist with id {playlist_data.playlist_id} does not exists'}, HTTPStatus.NOT_FOUND
    playlist = delete_playlist(get_db, GetPlaylist(playlist_id=request.args.get('playlist_id')))
    resp = PlaylistSchema(
        playlist_description=playlist.playlist_description,
        playlist_id=playlist.playlist_id,
        playlist_title=playlist.playlist_title,
        playlist_thumbnail=playlist.playlist_thumbnail,
        published_at=playlist.published_at,
        privacy_status=playlist.privacy_status,
        videos_count=playlist.videos_count,
        channel_id=playlist.channel_id
    )
    return resp.model_dump_json(indent=4), HTTPStatus.OK


@swag_from("./docs/get.yml", endpoint="playlists.get", methods=["GET"])
@playlists.route("/playlist", methods=["GET"])
def get():
    try:
        playlist_data = GetPlaylist(playlist_id=request.args.get('playlist_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the playlist id.'}, HTTPStatus.BAD_REQUEST
    playlist = get_playlist(session=get_db, playlist_data=playlist_data)
    if playlist:
        resp = PlaylistSchema(
            playlist_description=playlist.playlist_description,
            playlist_id=playlist.playlist_id,
            playlist_title=playlist.playlist_title,
            playlist_thumbnail=playlist.playlist_thumbnail,
            published_at=playlist.published_at,
            privacy_status=playlist.privacy_status,
            videos_count=playlist.videos_count,
            channel_id=playlist.channel_id
        )
        return resp.model_dump_json(indent=4), HTTPStatus.OK
    
    return {'Error':f'No channel with id {playlist_data.playlist_id}'}, HTTPStatus.NOT_FOUND


@playlists.route("/", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add_many.yml", endpoint="playlists.add_many", methods=["POST"])
def add_many():
    try:
        playlists_data = [PlaylistSchema(**data) for data in request.json['playlists']]
        playlists = PlaylistsSchema(playlists=playlists_data)
    except ValidationError:
        return {'Error': 'Invalid playlist data!'}, HTTPStatus.BAD_REQUEST
    count: int = create_many(session=get_db, playlists_data=playlists)
    return {'Success':f'{count} playlist(s) added.'}, HTTPStatus.CREATED


@swag_from("./docs/playlists.yml", endpoint="playlists.list_all_playlists", methods=["GET"])
@playlists.route("/", methods=["GET"])
def list_all_playlists():
    offset: str = request.args.get('offset')
    limit: str = request.args.get('limit')
    playlists = get_playlists(get_db, GetPlaylists(offset=offset, limit=limit))
    playlists = [
        PlaylistSchema(
            playlist_description=playlist.playlist_description,
            playlist_id=playlist.playlist_id,
            playlist_title=playlist.playlist_title,
            playlist_thumbnail=playlist.playlist_thumbnail,
            published_at=playlist.published_at,
            privacy_status=playlist.privacy_status,
            videos_count=playlist.videos_count,
            channel_id=playlist.channel_id
        ).dict()
        for playlist in playlists
    ]
    return playlists, HTTPStatus.OK


@swag_from("./docs/playlist_videos.yml", endpoint="playlists.videos", methods=["GET"])
@playlists.route("/playlist/videos", methods=["GET"])
def videos():
    return {'success':'playlist'}, HTTPStatus.CREATED
