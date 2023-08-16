from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Video(BaseModel):
    video_id: str
    video_title: str
    channel_id: str
    published_at: datetime
    custom_url: str
    video_description: str
    video_thumbnail: str
    views_count: int
    likes_count: int
    comments_count: int
    video_duration: str
    
class Videos(BaseModel):
    videos: list[Video]
    
class GetVideo(BaseModel):
    video_id: str
    
class GetVideos(BaseModel):
    offset: Optional[int] = 0
    limit: Optional[int] = 10