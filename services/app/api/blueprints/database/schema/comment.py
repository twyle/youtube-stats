from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AuthorBase(BaseModel):
    author_profile_image_url: str
    author_channel_url: str
    author_channel_id: str
    author_display_name: str
    
class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    author_id: int
    
class CommentBase(BaseModel):
    comment_id: str
    video_id: str
    parent_id: Optional[str]
    comment_text: str
    like_count: int
    published_at: datetime
    updated_at: datetime
    
class CommentCreate(CommentBase):
    author: AuthorCreate
    
class Comment(CommentBase):
    author_id: int

class CommentsCreate(BaseModel):
    comments: list[CommentCreate]

class Comments(BaseModel):
    comments: list[Comment]
    
class GetComment(BaseModel):
    comment_id: str
    
class GetComments(BaseModel):
    offset: Optional[int] = 0
    limit: Optional[int] = 10