from http import HTTPStatus
from sqlalchemy.orm import Session
from ..models.playlist import Playlist
from ..schema.playlist import (
    Playlist as PlaylistSchema, Playlists as PlaylistsSchema, GetPlaylist, GetPlaylists
    )
from sqlalchemy.exc import IntegrityError


def create_playlist(playlist_data: PlaylistSchema, session: Session):
    playlist = Playlist(
        playlist_description=playlist_data.playlist_description,
        playlist_id=playlist_data.playlist_id,
        playlist_title=playlist_data.playlist_title,
        playlist_thumbnail=playlist_data.playlist_thumbnail,
        published_at=playlist_data.published_at,
        privacy_status=playlist_data.privacy_status,
        videos_count=playlist_data.videos_count,
        channel_id=playlist_data.channel_id
    )
    with session() as db:
        db.add(playlist)
        db.commit()
        db.refresh(playlist)
    return playlist


def create_many(session: Session, playlists_data: PlaylistsSchema):
    count: int = 0
    with session() as db:
        for playlist in playlists_data.playlists:
            playlist = Playlist(
                playlist_description=playlist.playlist_description,
                playlist_id=playlist.playlist_id,
                playlist_title=playlist.playlist_title,
                playlist_thumbnail=playlist.playlist_thumbnail,
                published_at=playlist.published_at,
                privacy_status=playlist.privacy_status,
                videos_count=playlist.videos_count,
                channel_id=playlist.channel_id
            )
            try:
                db.add(playlist)
                db.commit()
                count += 1
            except IntegrityError:
                pass
    return count

def get_playlist(session: Session, playlist_data: GetPlaylist):
    with session() as db:
        playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_data.playlist_id).first()
    return playlist

def get_playlists(session: Session, playlist_data: GetPlaylists):
    with session() as db:
        playlists = db.query(Playlist).offset(playlist_data.offset).limit(playlist_data.limit).all()
    return playlists

def delete_playlist(session: Session, playlist_data: GetPlaylist):
    with session() as db:
        playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_data.playlist_id).first()
        db.delete(playlist)
        db.commit()
        
    return playlist