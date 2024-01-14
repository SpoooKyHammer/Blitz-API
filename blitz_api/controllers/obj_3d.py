
from flask import Blueprint, request, abort
from marshmallow import Schema, fields, ValidationError
import base64
import io
from PIL import Image
from blitz_api.db import DataBase
from bson.objectid import ObjectId

bp_3d_obj = Blueprint("3d_obj", __name__, url_prefix="/3d_obj")

class RequestBodySchema(Schema):
    """
    Request Body declaration for `/3d_obj/create` endpoint.
    """
    
    image_name = fields.String(required=True)
    extension = fields.String(required=True)
    image_base64 = fields.String(required=True)


@bp_3d_obj.route("/create", methods=["POST"])
def create_3d_obj():
    content_type = request.headers.get("Content-Type")

    if content_type != "application/json":
        abort(415)
     
    try:     
        request_body_schema = RequestBodySchema()
        request_body_schema.load(request.json)
    except ValidationError:
        abort(400, description="Invalid Request Body")
    
    image_base64_str = request.json["image_base64"]
    image_extension = request.json["extension"]
    image_name = request.json["image_name"]
    image = Image.open(io.BytesIO(base64.decodebytes(bytes(image_base64_str, "utf-8"))))
    image.save(f"{image_name}.{image_extension}")
    
    image = open(f"{image_name}.{image_extension}", "rb")
    _id = DataBase.get_gridFs().put(image, filename=f"{image_name}.{image_extension}")
    image.close()

    return { "msg": "successfully saved file", "_id": str(_id) }

@bp_3d_obj.route("/delete/<_id>", methods=["DELETE"])
def delete_3d_obj(_id):
    file_exists = DataBase.get_gridFs().exists(ObjectId(_id))
    if file_exists:
        DataBase.get_gridFs().delete(ObjectId(_id))
        return { "msg": "successfully deleted file", "_id": _id }
    else:
        return "", 204
