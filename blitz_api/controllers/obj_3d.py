
import base64
import io
import pathlib
from PIL import Image

from flask import Blueprint, request, abort
from marshmallow import Schema, fields, ValidationError
from bson.objectid import ObjectId

from blitz_api.db import DataBase


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
        RequestBodySchema().load(request.json)
    except ValidationError:
        abort(400, description="Invalid Request Body")
    
    image_base64_str = request.json["image_base64"]
    image_extension = request.json["extension"]
    image_name = request.json["image_name"]

    image = Image.open(io.BytesIO(base64.decodebytes(bytes(image_base64_str, "utf-8"))))
    dumps_path = pathlib.Path().cwd().joinpath("dumps")
    image.save(f"{dumps_path}/{image_name}.{image_extension}")
    
    image = open(f"{dumps_path}/{image_name}.{image_extension}", "rb")
    _id = DataBase.get_gridFs().put(image, filename=f"{image_name}.{image_extension}") 
    image.close()

    dumps_path.joinpath(f"{image_name}.{image_extension}").unlink(True)

    return { "msg": "successfully saved file", "_id": str(_id) }

@bp_3d_obj.route("/delete/<_id>", methods=["DELETE"])
def delete_3d_obj(_id):
    file_exists = DataBase.get_gridFs().exists(ObjectId(_id))
    if file_exists:
        DataBase.get_gridFs().delete(ObjectId(_id))
        return { "msg": "successfully deleted file", "_id": _id }
    else:
        return "", 204

@bp_3d_obj.route("/deleteAll", methods=["DELETE"])
def delete_all_files():
    cursor = DataBase.get_gridFs().find({})
    
    for grid_out in cursor:
        DataBase.get_gridFs().delete(grid_out._id)
    
    return { "msg": "successfully deleted all files" }
