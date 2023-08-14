"""This script launches the application."""
from api import create_app
# from api.helpers.add_channels import add_channel_playlists
from flask.cli import FlaskGroup
from api.blueprints.database.database import create_all
from api.blueprints.database.models.user import User

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("create_db")
def create_db():
    create_all()


# @cli.command("seed_db")
# def seed_db():
#     """Create the database records."""
#     add_channel_playlists('UC5WVOSvL9bc6kwCMXXeFLLw')


if __name__ == "__main__":
    cli()
