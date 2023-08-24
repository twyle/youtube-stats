from elasticsearch import Elasticsearch
from elastic_transport import ApiError
from .....config.logger_config import app_logger

def create_playlist_index(es_client: Elasticsearch, playlists_index: str = 'playlists') -> None:
    body = {
        'mappings': {
            'properties': {
                'playlist_id': {'type': 'keyword'},
                'channel_id': {'type': 'keyword'},
                'playlist_title': {
                    'type': 'text',
                    'fields': {
                        'raw': {
                            'type': 'keyword'
                        }
                    }
                },
                'published_at': {'type': 'date'},
                'playlist_description': {'type': 'text'},
                'playlist_thumbnail': {'type': 'keyword'},
                'privacy_status': {'type': 'keyword'},
                'videos_count': {'type': 'long'}
            }
        }
    }
    try:
        es_client.indices.delete(index=playlists_index, ignore=[400, 404])
        es_client.indices.create(index=playlists_index, body=body)
    except ApiError:
        app_logger.error(f"Unable to create index '{playlists_index}'.")
    else:
        app_logger.info(f"Index '{playlists_index}' created succsefully.")
    