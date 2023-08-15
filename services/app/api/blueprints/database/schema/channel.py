from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Channel(BaseModel):
    channel_id: str
    channel_title: str
    published_at: datetime
    custom_url: str
    channel_description: str
    channel_thumbnail: str
    views_count: int
    videos_count: int
    subscribers_count: int
    
class Channels(BaseModel):
    channels: list[Channel]
    
class GetChannel(BaseModel):
    channel_id: str
    
class GetChannels(BaseModel):
    offset: Optional[int] = 0
    limit: Optional[int] = 10