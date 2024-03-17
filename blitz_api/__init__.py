
from flask import Flask, config 
from flasgger import Swagger

from . import controllers
from .ext import DataBase, create_celery
from .config.swagger import template, swagger_config 
from .config import Dev, Prod


def create_app(test_config=None) -> Flask:
    """Factory method that creates the application"""
    
    app = Flask(__name__)
    app.config["CELERY_CONFIG"] = {"broker_url": Prod.REDIS_URL, "result_backend": Prod.REDIS_URL, "task_ignore_result": True}

    Swagger(app, config=swagger_config, template=template)
    
    controllers.register_controllers(app)
    
    DataBase.init()
    
    create_celery(app)

    return app
