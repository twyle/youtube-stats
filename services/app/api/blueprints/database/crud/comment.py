from http import HTTPStatus
from sqlalchemy.orm import Session
from ..models.comment import Comment, CommentAuthor
from ..schema.comment import (
    CommentCreate, GetComment, GetComments, CommentsCreate
)
from sqlalchemy.exc import IntegrityError


def create_comment(comment_data: CommentCreate, session: Session):
    comment_author = CommentAuthor(**comment_data.author.model_dump())
    comment = Comment(**comment_data.model_dump(exclude={'author'}))
    comment.author = comment_author
    with session() as db:
        db.add(comment)
        db.commit()
        db.refresh(comment)
    return comment


def create_many(session: Session, comments_data: CommentsCreate):
    count: int = 0
    with session() as db:
        for comment_data in comments_data.comments:
            comment_author = CommentAuthor(**comment_data.author.model_dump())
            comment = Comment(**comment_data.model_dump(exclude={'author'}))
            comment.author = comment_author
            try:
                db.add(comment)
                db.commit()
                count += 1
            except IntegrityError:
                pass
    return count

def get_comment(session: Session, comment_data: GetComment):
    with session() as db:
        comment = db.query(Comment).filter(Comment.comment_id == comment_data.comment_id).first()
    return comment

def get_comments(session: Session, comment_data: GetComments):
    with session() as db:
        comments = db.query(Comment).offset(comment_data.offset).limit(comment_data.limit).all()
    return comments

def delete_comment(session: Session, comment_data: GetComment):
    with session() as db:
        comment = db.query(Comment).filter(Comment.comment_id == comment_data.comment_id).first()
        db.delete(comment)
        db.commit()
        
    return comment


# def get_channel_playlists(session: Session, channel_data: GetChannel):
#     playlists = []
#     with session() as db:
#         channel: Channel = db.query(Channel).filter(Channel.channel_id == channel_data.channel_id).first()
#         playlists = channel.playlists
#     return playlists


# def get_channel_videos(session: Session, channel_data: GetChannel):
#     videos = []
#     with session() as db:
#         channel: Channel = db.query(Channel).filter(Channel.channel_id == channel_data.channel_id).first()
#         videos = channel.videos
#     return videos
        