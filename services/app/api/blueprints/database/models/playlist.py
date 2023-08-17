from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Optional
from .video_playlist import VideoPlaylist


class Playlist(Base):
    __tablename__ = 'playlists'
    
    playlist_id: Mapped[str] = mapped_column(primary_key=True)
    playlist_title: Mapped[str]
    published_at: Mapped[datetime]
    channel_id: Mapped[str] = mapped_column(ForeignKey('channels.channel_id'))
    playlist_description: Mapped[str]
    playlist_thumbnail: Mapped[str]
    privacy_status: Mapped[Optional[str]] = 'public'
    videos_count: Mapped[Optional[int]] = 0
    
    channel = relationship('Channel', back_populates='playlists')
    videos = relationship(VideoPlaylist, back_populates='playlist')
