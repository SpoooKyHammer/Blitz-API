from flask import Blueprint, request, abort
from marshmallow import Schema, fields, ValidationError
import base64
import io
from PIL import Image
from blitz_api.db import DataBase


class RequestBodySchema(Schema):
    """
    Request Body declaration for `/generate` endpoint.
    """
    
    image_name = fields.String(required=True)
    extension = fields.String(required=True)
    image_base64 = fields.String(required=True)


gen = Blueprint("generate", __name__)

@gen.route("/generate", methods=["POST"])
def generate():
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
    DataBase.get_gridFs().put(image, filename=f"{image_name}.{image_extension}")
    image.close()

    return "Success"
