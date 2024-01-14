from flask import Flask, Blueprint
from .obj_3d import bp_3d_obj

def register_controllers(app: Flask) -> None:
    """Registers all controllers."""
    
    api = Blueprint("api", __name__, url_prefix="/api/v1")
    api.register_blueprint(bp_3d_obj)
    app.register_blueprint(api)
