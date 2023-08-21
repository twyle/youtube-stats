from ....extensions.extensions import es_client
from ....config.config import BaseConfig


def create_log_index():
    es_client.indices.delete(BaseConfig().LOG_INDEX, ignore=[400,404])
    es_client.indices.create(index=BaseConfig().LOG_INDEX)