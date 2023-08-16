from http import HTTPStatus
from sqlalchemy.orm import Session
from ..models.video import Video
from ..schema.video import (
    Video as VideoSchema, Videos as VideosSchema, GetVideo, GetVideos
    )
from sqlalchemy.exc import IntegrityError


def create_video(video_data: VideoSchema, session: Session):
    video = Video(
        channel_id=video_data.channel_id,
        video_description=video_data.video_description,
        video_id=video_data.video_id,
        video_title=video_data.video_title,
        video_thumbnail=video_data.video_thumbnail,
        published_at=video_data.published_at,
        views_count=video_data.views_count,
        likes_count=video_data.likes_count,
        comments_count=video_data.comments_count,
        video_duration=video_data.video_duration
    )
    with session() as db:
        db.add(video)
        db.commit()
        db.refresh(video)
    return video


def create_many(session: Session, videos_data: VideosSchema):
    count: int = 0
    with session() as db:
        for video in videos_data.videos:
            video = Video(
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
            try:
                db.add(video)
                db.commit()
                count += 1
            except IntegrityError:
                pass
    return count

def get_video(session: Session, video_data: GetVideo):
    with session() as db:
        video = db.query(Video).filter(Video.video_id == video_data.video_id).first()
    return video

def get_videos(session: Session, video_data: GetVideos):
    with session() as db:
        videos = db.query(Video).offset(video_data.offset).limit(video_data.limit).all()
    return videos

def delete_video(session: Session, video_data: GetVideo):
    with session() as db:
        video = db.query(Video).filter(Video.video_id == video_data.video_id).first()
        db.delete(video)
        db.commit()
        
    return video