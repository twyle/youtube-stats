from elasticsearch import Elasticsearch
from elastic_transport import ApiError
from .....config.logger_config import app_logger

def create_video_index(es_client: Elasticsearch, videos_index: str = 'videos') -> None:
    body = {
        'mappings': {
            'properties': {
                'video_id': {'type': 'keyword'},
                'channel_id': {'type': 'keyword'},
                'video_title': {
                    'type': 'text',
                    'fields': {
                        'raw': {
                            'type': 'keyword'
                        }
                    }
                },
                'published_at': {'type': 'date'},
                'video_duration': {'type': 'keyword'},
                'video_description': {'type': 'text'},
                'video_thumbnail': {'type': 'keyword'},
                'views_count': {'type': 'long'},
                'likes_count': {'type': 'long'},
                'comments_count': {'type': 'long'},
                'comments': {
                    'type': 'nested',
                    'properties': {
                        'parent_id': {'type': 'keyword'},
                        'comment_text': {'type': 'text'},
                        'like_count': {'type': 'long'},
                        'published_at': {'type': 'date'},
                        'updated_at': {'type': 'date'}
                    }
                }
            }
        }
    }
    try:
        es_client.indices.delete(index=videos_index, ignore=[400, 404])
        es_client.indices.create(index=videos_index, body=body)
    except ApiError:
        app_logger.error(f"Unable to create index '{videos_index}'.")
    else:
        app_logger.info(f"Index '{videos_index}' created succsefully.")
    