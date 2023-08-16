from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime


class Video(Base):
    __tablename__ = 'videos'
    
    video_id: Mapped[str] = mapped_column(primary_key=True)
    video_title: Mapped[str]
    channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'))
    published_at: Mapped[datetime]
    video_description: Mapped[str]
    video_thumbnail: Mapped[str]
    views_count: Mapped[int]
    likes_count: Mapped[int]
    comments_count: Mapped[int]
    video_duration: Mapped[str]
    
    channel = relationship('Channel', back_populates='videos')
    comments = relationship('Comment', back_populates='video')
    playlists = relationship('VideoPlaylist', back_populates='video')
    