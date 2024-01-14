from flask import Flask 
from . import controllers
from .db import DataBase


def create_app(test_config=None):
    app = Flask(__name__)
    controllers.register_controllers(app)
    DataBase.init()
    return app
