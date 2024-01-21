
import base64
import io
import pathlib
from PIL import Image

from flask import Blueprint, request, abort
from marshmallow import Schema, fields, ValidationError
from bson.objectid import ObjectId

from blitz_api.db import DataBase


class RequestBodySchema(Schema):
    """
    Request Body declaration for `/3d_obj/create` endpoint.
    """
    
    image_name = fields.String(required=True)
    extension = fields.String(required=True)
    image_base64 = fields.String(required=True)


bp_3d_obj = Blueprint("3d_obj", __name__, url_prefix="/3d_obj")

@bp_3d_obj.route("/create", methods=["POST"])
def create_3d_obj():
    """
    Create 3D object 
    Creates a `.obj` file and saves it into database with the `filename` field as the one passed as `image_name` in body. 
    ---
    tags:
        - 3D object
    parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          image_name:
            type: string
            example: walking pose
          extension:
            type: string
            example: png
          image_base64:
            type: string
            example: iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII=

    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            msg:
              type: string
              example: successfully saved file 
            _id:
              type: string
              example: 65acd0610a73b4382f214682

      400:
        description: Invalid request body

      415:
        description: Unsupported content type
    """

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
    """
    Delete file
    Delete a file by their respective MongoDB `_id`.
    ---
    tags:
      - 3D object
    parameters:
    - in: _id
      name: _id
      required: true
      description: MongoDB `_id` of the document to delete.
      schema:
        type: string
        example: 65acd0610a73b4382f214682

    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            msg:
              type: string
              example: successfully deleted file 
            _id:
              type: string
              example: 65acd0610a73b4382f214682

      204:
        description: Success
    """

    file_exists = DataBase.get_gridFs().exists(ObjectId(_id))
    if file_exists:
        DataBase.get_gridFs().delete(ObjectId(_id))
        return { "msg": "successfully deleted file", "_id": _id }
    else:
        return "", 204

@bp_3d_obj.route("/deleteAll", methods=["DELETE"])
def delete_all_files():
    """
    Deletes all files stored in database
    ---
    tags:
      - 3D object

    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            msg:
              type: string
              example: successfully deleted all files
    """
    cursor = DataBase.get_gridFs().find({})
    
    for grid_out in cursor:
        DataBase.get_gridFs().delete(grid_out._id)
    
    return { "msg": "successfully deleted all files" }
