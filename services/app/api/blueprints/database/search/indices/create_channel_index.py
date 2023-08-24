from elasticsearch import Elasticsearch
from elastic_transport import ApiError
from .....config.logger_config import app_logger

def create_channel_index(es_client: Elasticsearch, channels_index: str = 'channels') -> None:
    body = {
        'mappings': {
            'properties': {
                'channel_id': {'type': 'keyword'},
                'channel_title': {
                    'type': 'text',
                    'fields': {
                        'raw': {
                            'type': 'keyword'
                        }
                    }
                },
                'published_at': {'type': 'date'},
                'custom_url': {'type': 'keyword'},
                'channel_description': {'type': 'text'},
                'channel_thumbnail': {'type': 'keyword'},
                'views_count': {'type': 'long'},
                'videos_count': {'type': 'long'},
                'subscribers_count': {'type': 'long'}
            }
        }
    }
    try:
        es_client.indices.delete(index=channels_index, ignore=[400, 404])
        es_client.indices.create(index=channels_index, body=body)
    except ApiError:
        app_logger.error(f"Unable to create index '{channels_index}'.")
    else:
        app_logger.info(f"Index '{channels_index}' created succsefully.")
    