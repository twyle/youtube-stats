from flasgger import swag_from
from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..database.crud.channel import (
    create_channel, create_many, get_channel, delete_channel, get_channels
)
from ..database.schema.channel import (
    Channel as ChannelSchema, Channels as ChannelsSchema, GetChannel, GetChannels
)
from ..database.database import get_db
from http import HTTPStatus
from pydantic import ValidationError
from flask import request

#from ..decorators import admin_token_required

channels = Blueprint("channels", __name__)


@channels.route("/channel", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add.yml", endpoint="channels.add", methods=["POST"])
def add():
    try:
        channel_data = ChannelSchema(**request.json)
    except ValidationError:
        return {'Error': 'Invalid channel data!'}, HTTPStatus.BAD_REQUEST
    channel = get_channel(session=get_db, channel_data=channel_data)
    if channel:
        return {'Error': f'channel with id {channel_data.channel_id} already exists'}, HTTPStatus.CONFLICT
    channel = create_channel(channel_data=channel_data, session=get_db)
    resp = ChannelSchema(
        channel_description=channel.channel_description,
        channel_id=channel.channel_id,
        channel_title=channel.channel_title,
        channel_thumbnail=channel.channel_thumbnail,
        published_at=channel.published_at,
        views_count=channel.views_count,
        videos_count=channel.videos_count,
        subscribers_count=channel.subscribers_count,
        custom_url=channel.custom_url
    )
    
    return resp.model_dump_json(indent=4), HTTPStatus.CREATED


@channels.route("/channel", methods=["PUT"])
# @admin_token_required
@swag_from("./docs/update.yml", endpoint="channels.update", methods=["PUT"])
def update():
    return {'success':'channel'}, HTTPStatus.CREATED


@channels.route("/channel", methods=["DELETE"])
# @admin_token_required
@swag_from("./docs/delete.yml", endpoint="channels.delete", methods=["DELETE"])
def delete():
    try:
        channel_data = GetChannel(channel_id=request.args.get('channel_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the channel id.'}, HTTPStatus.BAD_REQUEST
    channel = get_channel(session=get_db, channel_data=channel_data)
    if not channel:
        return {'Error': f'channel with id {channel_data.channel_id} does not exists'}, HTTPStatus.NOT_FOUND
    channel = delete_channel(get_db, GetChannel(channel_id=request.args.get('channel_id')))
    resp = ChannelSchema(
        channel_description=channel.channel_description,
        channel_id=channel.channel_id,
        channel_title=channel.channel_title,
        channel_thumbnail=channel.channel_thumbnail,
        published_at=channel.published_at,
        views_count=channel.views_count,
        videos_count=channel.videos_count,
        subscribers_count=channel.subscribers_count,
        custom_url=channel.custom_url
    )
    return resp.model_dump_json(indent=4), HTTPStatus.OK


@channels.route("/channel", methods=["GET"])
# @admin_token_required
@swag_from("./docs/get.yml", endpoint="channels.get", methods=["GET"])
def get():
    try:
        channel_data = GetChannel(channel_id=request.args.get('channel_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the channel id.'}, HTTPStatus.BAD_REQUEST
    channel = get_channel(session=get_db, channel_data=channel_data)
    if channel:
        resp = ChannelSchema(
            channel_description=channel.channel_description,
            channel_id=channel.channel_id,
            channel_title=channel.channel_title,
            channel_thumbnail=channel.channel_thumbnail,
            published_at=channel.published_at,
            views_count=channel.views_count,
            videos_count=channel.videos_count,
            subscribers_count=channel.subscribers_count,
            custom_url=channel.custom_url
        )
        return resp.model_dump_json(indent=4), HTTPStatus.OK
    
    return {'Error':f'No channel with id {channel_data.channel_id}'}, HTTPStatus.NOT_FOUND


@channels.route("/", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add_many.yml", endpoint="channels.add_many", methods=["POST"])
def add_many():
    channels_data = [ChannelSchema(**data) for data in request.json['channels']]
    channels = ChannelsSchema(channels=channels_data)
    count: int = create_many(session=get_db, channels_data=channels)
    return {'Success':f'{count} channel(s) added.'}, HTTPStatus.CREATED


@channels.route("/", methods=["GET"])
# @jwt_required()
@swag_from("./docs/channels.yml", endpoint="channels.list_all_channels", methods=["GET"])
def list_all_channels():
    offset: str = request.args.get('offset')
    limit: str = request.args.get('limit')
    channels = get_channels(get_db, GetChannels(offset=offset, limit=limit))
    channels = [
        ChannelSchema(
            channel_description=channel.channel_description,
            channel_id=channel.channel_id,
            channel_title=channel.channel_title,
            channel_thumbnail=channel.channel_thumbnail,
            published_at=channel.published_at,
            views_count=channel.views_count,
            videos_count=channel.videos_count,
            subscribers_count=channel.subscribers_count,
            custom_url=channel.custom_url
        ).dict()
        for channel in channels
    ]
    return channels, HTTPStatus.OK


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
