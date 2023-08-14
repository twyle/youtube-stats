# youtube-video-stats

> An API that provides data on YouTube videos posted by kenyan influencers.

<p align="center">
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/Medium-Clone-Blog-Service/actions/workflows/feature-development-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/Medium-Clone-Blog-Service/actions/workflows/development-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/Medium-Clone-Blog-Service/actions/workflows/staging-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/Medium-Clone-Blog-Service/actions/workflows/release-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/Medium-Clone-Blog-Service/actions/workflows/production-workflow.yml/badge.svg" />
  <a href='https://youtube-video-stats.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/youtube-video-stats/badge/?version=latest' alt='Documentation Status' />
</a>
  <a href='https://youtube-video-stats.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/youtube-video-stats/badge/?version=latest' alt='Documentation Status' />
</a>
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/security-bandit-yellow.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Made%20with- Python-1f425f.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/github/license/Naereen/StrapDown.js.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Medium-12100E?style=flat&logo=medium&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/github%20actions-%232671E5.svg?style=flat&logo=githubactions&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=flat&logo=visual-studio-code&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/gunicorn-%298729.svg?style=flat&logo=gunicorn&logoColor=white" />
</p>

## Application Overview

This an API that provides data on the videos posted by Kenyan Social media influencers on YouTube. This includes all the videos posted in their respective youtube channels and includes stats such as date posted, number of views, likes, as well as the video comments.

<img src="assets/images/video-stats.png" class="img-responsive" alt="">

### API Endpoints

The API provides various endpoints for various uses:

1. Admin endpoint for administrative tasks such as registering new administrators.
2. Authentication endpoint for registering new users, activating user account, generating access tokens and updating user details.
3. Channels endpoint for getting data on channels.
4. Comment Authors endpoint provides data on the various people who've commented on a given video.
5. Comments endpoint for gathering data on comments for videos and channels.
6. Playlist Items endpoint provides data on the items found in various playlists.
7. The Playlists endpoint provides data on the various playlists.
8. The videos endpoint provides data on the videos.

<p align=center>
  <img src="assets/videos/video.gif" />
</p>

### API Documentation

To learn more about this API, including the routes and authentication, read the [official documentation](https://youtube-video-stats.readthedocs.io/en/latest/).

### Security

The various endpoints are protected. Access will require either an ``access_token`` or ``admin_token`` both of which are provided upon registration. All routes that create, delete or update a resource are protected by an admin token, whereas getting a resource only needs an access token.

## Getting Started

- This API has been tested on Ubuntu 22.04 with Python 3.10+
- It uses SQLite database by default, witth raw sql queries. Implementation that uses an ORM with PostgreSQL is under development.
- The application is containerized, so ensure docker and docker compose are installed in your computer.

To test out the application locally:

1. Clone the project repo:

```sh
  git clone https://github.com/twyle/youtube-video-stats.git
```

2. Navigate to the project directory, then create the project secrets:

```sh
  cd youtube-video-stats
  touch ./services/app/.env
```

  Then paste the following:

```sh
  FLASK_APP=manage.py
  FLASK_DEBUG=True
  FLASK_ENV=development
  SECRET_KEY=df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506
```

3. Start the application:

```sh
  docker-compose -f docker-compose-dev up --build -d
```

4. Navigate to ``localhost:5000/apidocs`` to use the deployed application.

### Testing the application

To test out the application, we need to seed the database with some data and create and activate a user account. We will also need an admin account for us to be able to add data to the database.

#### Creating an Admin

Make sure to store the admin token.

<p align=center>
  <img src="assets/videos/admin.gif" />
</p>

### Seeding the database

For this we will use a python library called ``ayv`` to obtain the various data points that we need from YouTube. In this example we will add a couple of channels.

You can read more about ``ayv`` from its documentation site:
[ayv documentation](https://youtube-wrapper.readthedocs.io/en/latest/)

#### Install ``ayv``

1. Create a python3 virtual environment

```sh
python3 -m venv venv
```

2. Install ``ayv``

```sh
pip install ayv
```

#### Get channel data

To use the ``ayv`` library to obtain channel data, we need the channel id. We can get the channel id by obtaining it from videos belonginging to the channel.
Here is an example script that uses a video id to fetch channel details including the title and id then saves them to disk:

```python
from youtube import YouTube
import json
import os
from typing import Optional
from youtube.models.video_model import Video

client_secrets_file = '/home/lyle/Downloads/temp.json'
youtube = YouTube(client_secrets_file)
youtube.authenticate()

def save_to_channels(video: Video, file_name: Optional[str] = "kenyan_channels.json") -> None:
    kenyan_channels = []
    if video:
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                try:
                    kenyan_channels = json.loads(f.read())
                except json.decoder.JSONDecodeError:
                    pass
        with open(file_name, 'w', encoding='utf-8') as f:
            data = {
                video.channel_title: video.channel_id
            }
            if not data in kenyan_channels:
                kenyan_channels.append(data)
            f.write(json.dumps(kenyan_channels, indent=2))
```

Simply call the function with the video id for a channel whose details you want.

Within ``youtube-video-stats/services/app`` is a file called ``kenyan_channels.json`` with a bunch of channel ids that we will use.

#### Add channel data

Here we will add a bunch of channels to the database:

```python

def find_channel(channel_id: str) -> Channel:
    """Find a channel with the given id."""
    channel = youtube.find_channel_by_id(channel_id)
    return channel

def post_data(data: dict[str, int|str], url: str) -> dict[str, str]:
    admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODU1MjAxOTcsImlhdCI6MTY4NDkxNTM5Nywic3ViIjoyfQ.hne-aXvET8nSwzK1EVtC3-0hPZE_Sa4njp8ZH1u7rkk"
    headers = {"Authorization": f"Bearer {admin_token}"}

    resp = requests.post(url, json=data, headers=headers)
    return resp

def load_channels(file: str) -> list[str]:
    """Load channel ids."""
    channel_ids: list[str] = []
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            channel_list: list[dict[str, str]] = json.loads(f.read())
            for data in channel_list:
                channel_ids.append(list(data.values())[0])
    return channel_ids

def create_channels(file: str) -> None:
    """Create the channels."""
    channel_ids = load_channels(file)
    channels = []
    for channel_id in channel_ids:
        channel = find_channel(channel_id)
        channels.append(channel.to_dict())
    data = {
        'channels': channels
    }
    url = 'http://localhost:5000/api/v1/channels/'
    resp = post_data(url=url, data=data)
    print(resp.json())

```

Call the ``create_channels`` function with a path to the ``kenyan_channels.json`` file. This will adfd the channels to the database. Make sure to replace the admin token.

#### Creating a User

To use the API, you will need an activated user account. This involves:

1. Creating a user account
2. Activating the account
3. Logging in to obtain an access token

<p align=center>
  <img src="assets/videos/register.gif" />
</p>

#### Listing Channels

To list the channels added, you need to authorize your requests.

<p align=center>
  <img src="assets/videos/channels.gif" />
</p>

## Deployment

- The application is containerized and deployed using an AWS EC2 instance.
- It uses the SQLite database.
- Uses AWS Route53 to route internet traffic to the application.
- It uses gunicorn with traefik.
- The application is auto-deployed to AWS once the production checks pass.

 To try out the API, head over to the [YouTube Stats API](https://youtube-stats.oryks-sytem.com/apidocs/).

## How to Contribute

To contribute, chack out the [contribution guideline](CONTRIBUTING.md).

## License

The API uses an [MIT License](LICENSE)

## Developer

Lyle Okoth – [@lylethedesigner](https://twitter.com/lylethedesigner) on twitter

[lyle okoth](https://medium.com/@lyle-okoth) on medium

My email is lyceokoth@gmail.com

Here is my [GitHub Profile](https://github.com/twyle/)

You can also find me on [Linkedin](https://www.linkedin.com/in/lyle-okoth/)
