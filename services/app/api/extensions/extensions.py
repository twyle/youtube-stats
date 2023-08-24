from flasgger import LazyString, Swagger
from flask import request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from elasticsearch import Elasticsearch
from ..config.config import BaseConfig

bcrypt = Bcrypt()
jwt = JWTManager()

def create_es_client():
    """Create the elasticsearch client."""
    ES_HOST = BaseConfig().ES_HOST
    ES_PORT = BaseConfig().ES_PORT
    es_client = Elasticsearch(hosts=[f'http://{ES_HOST}:{ES_PORT}'])
    return es_client

es_client = create_es_client()

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Kenyan Influencers YouTube Video Data..",
        "description": "An API for finding data on YouTube videos posted by Kenyan Influencers.",
        "contact": {
            "responsibleOrganization": "Oryks Systems",
            "responsibleDeveloper": "Lyle Okoth",
            "email": "lyceokoth@gmail.com",
            "url": "www.twitter.com/lylethedesigner",
        },
        "termsOfService": "www.twitter.com/deve",
        "version": "1.0",
    },
    "host": LazyString(lambda: request.host),
    "basePath": "/",  # base bash for blueprint registration
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "APIKeyHeader": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT Authorization header using the Bearer scheme. Example:"Authorization: Bearer {token}"',
        }
    },
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

swagger = Swagger(template=swagger_template, config=swagger_config)
