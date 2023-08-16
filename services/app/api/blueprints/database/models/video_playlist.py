from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class VideoPlaylist(Base):
    __tablename__ = 'video_playlist'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[str] = mapped_column(ForeignKey('videos.video_id'))
    playlist_id: Mapped[str] = mapped_column(ForeignKey('playlists.playlist_id'))