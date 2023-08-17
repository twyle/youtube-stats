from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey
from typing import Optional


class CommentAuthor(Base):
    __tablename__ = 'authors'
   
    author_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    author_profile_image_url: Mapped[str]
    author_channel_url: Mapped[str]
    author_channel_id: Mapped[str]
    author_display_name: Mapped[str]
    
    comments = relationship('Comment', back_populates='author')
    
    
class Comment(Base):
    __tablename__ = 'comments'
    
    comment_id: Mapped[str] = mapped_column(primary_key=True)
    video_id: Mapped[str] = mapped_column(ForeignKey('videos.video_id'))
    author_id: Mapped[str] = mapped_column(ForeignKey('authors.author_id'), init=False)
    parent_id: Mapped[Optional[str]]
    comment_text: Mapped[str]
    like_count: Mapped[int]
    published_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    
    video = relationship('Video', back_populates='comments')
    author = relationship('CommentAuthor', back_populates='comments')