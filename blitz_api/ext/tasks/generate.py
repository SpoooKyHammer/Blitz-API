
import base64
import io
import pathlib
from PIL import Image
from typing import Mapping

from celery import shared_task
from blitz_api.ext.db import DataBase
from blitz_api.ext.tasks.models.human_pose_estimation.rect import get_rect
from blitz_api.ext.tasks.models.pifuhd.apps.make import make_obj


@shared_task(ignore_result=False)
def generate_obj(image_id: str, name: str, extension: str, image_base64: str) -> Mapping[str, str]:
    """
    Creates a 3d object from an image using PIFuHD and human_pose_estimation model.

    Parameters
    ----------
        image_id: str
            ID of the image which will be used to index on the database.
        name: str
            Name of the image.
        extension: str
            Extension of the image file.
        image_base64: str
            Base64 data of the image.

    Returns
    -------
        dict: which has two key `_id` and `image_id`.
    """

    image = Image.open(io.BytesIO(base64.decodebytes(bytes(image_base64, "utf-8"))))
    dumps_path = pathlib.Path().cwd().joinpath("dumps/generate")
    image.save(f"{dumps_path}/{name}.{extension}")
    image_path = dumps_path.joinpath(f"{name}.{extension}")
    image.close()

    get_rect([str(image_path)], 512)

    resolution = 512
    make_obj(str(dumps_path), resolution)

    obj_file = open(f"result_{name}_{resolution}.obj", "rb")
    _id = DataBase.get_gridFs().put(obj_file, filename=f"{name}.obj", image_id=image_id) 
    obj_file.close()

    for file in dumps_path.iterdir():
        if file.name != ".gitkeep": file.unlink(True)

    return {"_id": str(_id), "image_id": image_id}

