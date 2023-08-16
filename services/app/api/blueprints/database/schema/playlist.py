from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Playlist(BaseModel):
    playlist_id: str
    playlist_title: str
    published_at: datetime
    channel_id: str
    playlist_description: str
    playlist_thumbnail: str
    privacy_status: str
    videos_count: int
    
class Playlists(BaseModel):
    playlists: list[Playlist]
    
class GetPlaylist(BaseModel):
    playlist_id: str
    
class GetPlaylists(BaseModel):
    offset: Optional[int] = 0
    limit: Optional[int] = 10