from http import HTTPStatus
from sqlalchemy.orm import Session
from ..models.channel import Channel
from ..schema.channel import (
    Channel as ChannelSchema, Channels as ChannelsSchema, GetChannel, GetChannels
    )
from sqlalchemy.exc import IntegrityError


def create_channel(channel_data: ChannelSchema, session: Session):
    channel = Channel(
        channel_description=channel_data.channel_description,
        channel_id=channel_data.channel_id,
        channel_title=channel_data.channel_title,
        channel_thumbnail=channel_data.channel_thumbnail,
        published_at=channel_data.published_at,
        views_count=channel_data.views_count,
        videos_count=channel_data.videos_count,
        subscribers_count=channel_data.subscribers_count,
        custom_url=channel_data.custom_url
    )
    with session() as db:
        db.add(channel)
        db.commit()
        db.refresh(channel)
    return channel


def create_many(session: Session, channels_data: ChannelsSchema):
    count: int = 0
    with session() as db:
        for channel in channels_data.channels:
            channel = Channel(
                channel_description=channel.channel_description,
                channel_id=channel.channel_id,
                channel_title=channel.channel_title,
                channel_thumbnail=channel.channel_thumbnail,
                published_at=channel.published_at,
                views_count=channel.views_count,
                videos_count=channel.videos_count,
                subscribers_count=channel.subscribers_count,
                custom_url=channel.custom_url
            )
            try:
                db.add(channel)
                db.commit()
                count += 1
            except IntegrityError:
                pass
    return count

def get_channel(session: Session, channel_data: GetChannel):
    with session() as db:
        channel = db.query(Channel).filter(Channel.channel_id == channel_data.channel_id).first()
    return channel

def get_channels(session: Session, channel_data: GetChannels):
    with session() as db:
        channels = db.query(Channel).offset(channel_data.offset).limit(channel_data.limit).all()
    return channels

def delete_channel(session: Session, channel_data: GetChannel):
    with session() as db:
        channel = db.query(Channel).filter(Channel.id == channel_data.channel_id).first()
        db.delete(channel)
        db.commit()
        
    return channel