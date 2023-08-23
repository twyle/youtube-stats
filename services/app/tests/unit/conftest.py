from . import create_app
import pytest
from . import (
    User, Video, Playlist, Channel
)
from . import create_all, drop_all

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(flask_env='test')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            drop_all()
            create_all()
            yield testing_client  
            
            
@pytest.fixture(scope='module')
def test_app():
    flask_app = create_app(flask_env='test')
    return flask_app