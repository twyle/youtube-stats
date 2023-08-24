"""This script launches the application."""
from api import create_app
from flask.cli import FlaskGroup
from api.blueprints.database.database import create_all
from api.blueprints.database.models import *
from api.extensions.extensions import es_client
from api.blueprints.database.search.indices import (
    create_playlist_index, create_channel_index, create_video_index
)

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("create_db")
def create_db():
    create_all()
    
    
@cli.command("create_indices")
def create_indices():
    create_channel_index(es_client=es_client)
    create_playlist_index(es_client=es_client)
    create_video_index(es_client=es_client)


if __name__ == "__main__":
    cli()
