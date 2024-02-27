
from flask import Flask, config 
from flasgger import Swagger

from . import controllers
from .ext import DataBase
from .config.swagger import template, swagger_config 


def create_app(test_config=None):
    """Factory method that creates the application"""
    
    app = Flask(__name__) 
    Swagger(app, config=swagger_config, template=template)
    controllers.register_controllers(app)
    DataBase.init()
    return app
