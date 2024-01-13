from flask import Flask, Blueprint 
from .controllers import hi, gen

def create_app(test_config=None):
    app = Flask(__name__)
    api = Blueprint("api", __name__, url_prefix="/api/v1")
    api.register_blueprint(hi)
    api.register_blueprint(gen)
    app.register_blueprint(api)

    return app
