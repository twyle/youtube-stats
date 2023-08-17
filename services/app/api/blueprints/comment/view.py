from flasgger import swag_from
from flask import Blueprint, request
from http import HTTPStatus
from ..database.crud.comment import (
    create_comment, get_comment, delete_comment, create_many, get_comments
)
from ..database.schema.comment import (
    CommentCreate, GetComment, Comment as CommentSchema, CommentsCreate, GetComments
)
from pydantic import ValidationError
from ..database.database import get_db


comments = Blueprint("comments", __name__)


@swag_from("./docs/add.yml", endpoint="comments.add", methods=["POST"])
@comments.route("/comment", methods=["POST"])
def add():
    try:
        comment_data = CommentCreate(**request.json)
    except ValidationError:
        return {'Error': 'Invalid comment data!'}, HTTPStatus.BAD_REQUEST
    comment = get_comment(session=get_db, comment_data=GetComment(comment_id=comment_data.comment_id))
    if comment:
        return {'Error': f'comment with id {comment_data.comment_id} already exists'}, HTTPStatus.CONFLICT
    comment = create_comment(comment_data=comment_data, session=get_db)
    resp = CommentSchema(
        comment_id=comment.comment_id,
        video_id=comment.video_id,
        parent_id=comment.parent_id,
        comment_text=comment.comment_text,
        like_count=comment.like_count,
        published_at=comment.published_at,
        updated_at=comment.updated_at,
        author_id=comment.author_id
    )
    return resp.model_dump_json(indent=4), HTTPStatus.CREATED


@swag_from("./docs/update.yml", endpoint="comments.update", methods=["PUT"])
@comments.route("/comment", methods=["PUT"])
def update():
    return {'comment': 'created'}, HTTPStatus.CREATED


@swag_from("./docs/delete.yml", endpoint="comments.delete", methods=["DELETE"])
@comments.route("/comment", methods=["DELETE"])
def delete():
    try:
        comment_data = GetComment(comment_id=request.args.get('comment_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the comment id.'}, HTTPStatus.BAD_REQUEST
    comment = get_comment(session=get_db, comment_data=comment_data)
    if not comment:
        return {'Error': f'comment with id {comment_data.comment_id} does not exists'}, HTTPStatus.NOT_FOUND
    comment = delete_comment(get_db, GetComment(comment_id=request.args.get('comment_id')))
    resp = CommentSchema(
        comment_id=comment.comment_id,
        video_id=comment.video_id,
        parent_id=comment.parent_id,
        comment_text=comment.comment_text,
        like_count=comment.like_count,
        published_at=comment.published_at,
        updated_at=comment.updated_at,
        author_id=comment.author_id
    )
    return resp.model_dump_json(indent=4), HTTPStatus.OK


@swag_from("./docs/get.yml", endpoint="comments.get", methods=["GET"])
@comments.route("/comment", methods=["GET"])
def get():
    return {'comment': 'created'}, HTTPStatus.CREATED


@comments.route("/", methods=["POST"])
# @admin_token_required
@swag_from("./docs/add_many.yml", endpoint="comments.add_many", methods=["POST"])
def add_many():
    comments_data = [CommentCreate(**data) for data in request.json['comments']]
    comments = CommentsCreate(comments=comments_data)
    count: int = create_many(session=get_db, comments_data=comments)
    return {'Success':f'{count} comment(s) added.'}, HTTPStatus.CREATED


@swag_from("./docs/comments.yml", endpoint="comments.list_all_comments", methods=["GET"])
@comments.route("/", methods=["GET"])
def list_all_comments():
    offset: str = request.args.get('offset')
    limit: str = request.args.get('limit')
    comments = get_comments(get_db, GetComments(offset=offset, limit=limit))
    comments = [
        CommentSchema(
            comment_id=comment.comment_id,
            video_id=comment.video_id,
            parent_id=comment.parent_id,
            comment_text=comment.comment_text,
            like_count=comment.like_count,
            published_at=comment.published_at,
            updated_at=comment.updated_at,
            author_id=comment.author_id
    ).model_dump()
        for comment in comments
    ]
    return comments, HTTPStatus.OK
