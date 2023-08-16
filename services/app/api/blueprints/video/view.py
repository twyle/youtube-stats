from flasgger import swag_from
from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..database.crud.video import (
    create_video, create_many, get_video, delete_video, get_videos
)
from ..database.schema.video import (
    Video as VideoSchema, Videos as VideosSchema, GetVideo, GetVideos
)
from ..database.schema.playlist import Playlist as PlaylistSchema
from ..database.database import get_db
from http import HTTPStatus
from pydantic import ValidationError
from flask import request

videos = Blueprint("videos", __name__)


@videos.route("/video", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add.yml", endpoint="videos.add", methods=["POST"])
def add():
    try:
        video_data = VideoSchema(**request.json)
    except ValidationError:
        return {'Error': 'Invalid video data!'}, HTTPStatus.BAD_REQUEST
    video = get_video(session=get_db, video_data=video_data)
    if video:
        return {'Error': f'video with id {video_data.video_id} already exists'}, HTTPStatus.CONFLICT
    video = create_video(video_data=video_data, session=get_db)
    resp = VideoSchema(
        channel_id=video.channel_id,
        video_description=video.video_description,
        video_id=video.video_id,
        video_title=video.video_title,
        video_thumbnail=video.video_thumbnail,
        published_at=video.published_at,
        views_count=video.views_count,
        likes_count=video.likes_count,
        comments_count=video.comments_count,
        video_duration=video.video_duration
    )
    
    return resp.model_dump_json(indent=4), HTTPStatus.CREATED


@videos.route("/", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add_many.yml", endpoint="videos.add_many", methods=["POST"])
def add_many():
    videos_data = [VideoSchema(**data) for data in request.json['videos']]
    videos = VideosSchema(videos=videos_data)
    count: int = create_many(session=get_db, videos_data=videos)
    return {'Success':f'{count} video(s) added.'}, HTTPStatus.CREATED


@videos.route("/video", methods=["GET"])
# @jwt_required()
@swag_from("./docs/get.yml", endpoint="videos.get", methods=["GET"])
def get():
    try:
        video_data = GetVideo(video_id=request.args.get('video_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the video id.'}, HTTPStatus.BAD_REQUEST
    video = get_video(session=get_db, video_data=video_data)
    if video:
        resp = VideoSchema(
            channel_id=video.channel_id,
            video_description=video.video_description,
            video_id=video.video_id,
            video_title=video.video_title,
            video_thumbnail=video.video_thumbnail,
            published_at=video.published_at,
            views_count=video.views_count,
            likes_count=video.likes_count,
            comments_count=video.comments_count,
            video_duration=video.video_duration
        )
        return resp.model_dump_json(indent=4), HTTPStatus.OK
    
    return {'Error':f'No video with id {video_data.video_id}'}, HTTPStatus.NOT_FOUND


@videos.route("/video", methods=["PUT"])
# @admin_token_required
@swag_from("./docs/update.yml", endpoint="videos.update", methods=["PUT"])
def update():
    return {'video':'succes'}, HTTPStatus.CREATED


@videos.route("/video", methods=["DELETE"])
# @admin_token_required
@swag_from("./docs/delete.yml", endpoint="videos.delete", methods=["DELETE"])
def delete():
    try:
        video_data = GetVideo(video_id=request.args.get('video_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the video id.'}, HTTPStatus.BAD_REQUEST
    video = get_video(session=get_db, video_data=video_data)
    if not video:
        return {'Error': f'video with id {video_data.video_id} does not exists'}, HTTPStatus.NOT_FOUND
    video = delete_video(get_db, GetVideo(video_id=request.args.get('video_id')))
    resp = VideoSchema(
        channel_id=video.channel_id,
        video_description=video.video_description,
        video_id=video.video_id,
        video_title=video.video_title,
        video_thumbnail=video.video_thumbnail,
        published_at=video.published_at,
        views_count=video.views_count,
        likes_count=video.likes_count,
        comments_count=video.comments_count,
        video_duration=video.video_duration
    )
    return resp.model_dump_json(indent=4), HTTPStatus.OK


@videos.route("/", methods=["GET"])
# @jwt_required()
@swag_from("./docs/videos.yml", endpoint="videos.list_all", methods=["GET"])
def list_all():
    offset: str = request.args.get('offset')
    limit: str = request.args.get('limit')
    videos = get_videos(get_db, GetVideos(offset=offset, limit=limit))
    videos = [
        VideoSchema(
            channel_id=video.channel_id,
            video_description=video.video_description,
            video_id=video.video_id,
            video_title=video.video_title,
            video_thumbnail=video.video_thumbnail,
            published_at=video.published_at,
            views_count=video.views_count,
            likes_count=video.likes_count,
            comments_count=video.comments_count,
            video_duration=video.video_duration
        ).dict()
        for video in videos
    ]
    return videos, HTTPStatus.OK


@videos.route("/video/comments", methods=["GET"])
# @jwt_required()
@swag_from("./docs/comments.yml", endpoint="videos.get_video_comments", methods=["GET"])
def get_video_comments():
    """Get the comments for a particular video."""
    return {'video':'succes'}, HTTPStatus.CREATED
