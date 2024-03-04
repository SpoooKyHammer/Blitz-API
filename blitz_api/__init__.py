
from flask import Flask, config 
from flasgger import Swagger

from . import controllers
from .ext import DataBase, create_celery
from .config.swagger import template, swagger_config 


def create_app(test_config=None) -> Flask:
    """Factory method that creates the application"""
    
    app = Flask(__name__)
    app.config["CELERY_CONFIG"] = {"broker_url": "redis://redis:6379", "result_backend": "redis://redis:6379", "task_ignore_result": True}

    Swagger(app, config=swagger_config, template=template)
    
    controllers.register_controllers(app)
    
    DataBase.init()
    
    create_celery(app)

    return app
