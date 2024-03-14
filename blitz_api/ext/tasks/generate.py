
import time
import base64
import io
import pathlib
from PIL import Image

from celery import shared_task
from blitz_api.ext.db import DataBase
from blitz_api.ext.tasks.models.human_pose_estimation.rect import get_rect


@shared_task(ignore_result=False)
def generate_3d_obj():
    time.sleep(20)
    return DataBase.get_gridFs().list()

@shared_task(ignore_result=False)
def generate(image_id: str, name: str, extension: str, image_base64: str) -> dict:
    image = Image.open(io.BytesIO(base64.decodebytes(bytes(image_base64, "utf-8"))))
    dumps_path = pathlib.Path().cwd().joinpath("dumps/generate")
    image.save(f"{dumps_path}/{name}.{extension}")

    image = open(f"{dumps_path}/{name}.{extension}", "rb")
    _id = DataBase.get_gridFs().put(image, filename=f"{name}.{extension}", image_id=image_id) 
    image.close()
    
    get_rect([dumps_path.joinpath(f"{name}.{extension}").__str__()], 512)
    
    dumps_path.joinpath(f"{name}.{extension}").unlink(True)

    return { 
            "msg": "successfully saved file",
            "_id": str(_id),
            "image_id": image_id,
            }
 
