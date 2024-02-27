
import base64
import io
import pathlib
from PIL import Image

from flask import Blueprint, request, abort, send_from_directory
from marshmallow import Schema, fields, ValidationError
from bson.objectid import ObjectId

from blitz_api.ext import DataBase

class RequestBodySchema(Schema):
    """
    Request Body declaration for `/3d_obj/create` endpoint.
    """
    
    extension = fields.String(required=True)
    image_name = fields.String(required=True)
    image_base64 = fields.String(required=True)
    image_id = fields.String(required=True)


bp_3d_obj = Blueprint("3d_obj", __name__, url_prefix="/3d_obj")

@bp_3d_obj.route("/download/<image_id>", methods=["GET"])
def download_obj(image_id):
    """
    Download file
    Downloads the `.obj` file on local machine.
    ---
    tags:
      - 3D object 
    parameters:
    - in: image_id
      name: image_id
      required: true
      description: The `image_id` of the `.obj` file to download.
      schema:
        type: string
        example: 65acd0610a73b4382f214682

    responses:
      200:
        description: Successfully downloaded the file on local machine.

      404:
        description: File not found to download. 
    """
    
    dumps_path = pathlib.Path().cwd().joinpath("dumps/downloads")

    for file in dumps_path.iterdir():
        if file.name == ".gitkeep": continue
        file.unlink()

    file = DataBase.get_gridFs().find_one({"image_id": image_id})
    
    if file is None:
        abort(404, description=f"FileNotFound\nThe requested file to download does not exist.")
    
    with open(f"{dumps_path}/{file.filename}", "wb") as file_buffer:
        file_buffer.write(file.read())

    filename = file.filename
    file.close()

    return send_from_directory(dumps_path, filename, as_attachment=True)

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
          extension:
            type: string
            example: png
          image_name:
            type: string
            example: walking pose
          image_base64:
            type: string
            example: iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII=
          image_id:
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
              example: successfully saved file 
            _id:
              type: string
              example: 65acd0610a73b4382f214682
            image_id:
              type: string
              example: 65acd0610a63b4382f214789
            download_link:
              type: string
              example: http://example.com/api/v1/3d_obj/download/65b64ba0409203f73b74d72 

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
    image_id = request.json["image_id"]

    image = Image.open(io.BytesIO(base64.decodebytes(bytes(image_base64_str, "utf-8"))))
    dumps_path = pathlib.Path().cwd().joinpath("dumps/generate")
    image.save(f"{dumps_path}/{image_name}.{image_extension}")

    image = open(f"{dumps_path}/{image_name}.{image_extension}", "rb")
    _id = DataBase.get_gridFs().put(image, filename=f"{image_name}.{image_extension}", image_id=image_id) 
    image.close()

    dumps_path.joinpath(f"{image_name}.{image_extension}").unlink(True)

    return { 
            "msg": "successfully saved file",
            "_id": str(_id),
            "image_id": image_id,
            "download_link": f"{request.root_url}api/v1{bp_3d_obj.url_prefix}/download/{image_id}"
            }

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

