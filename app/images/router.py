from fastapi import UploadFile
from fastapi import APIRouter
import shutil
from app.tasks.tasks import procces_picture


router = APIRouter(
    prefix="/images",
    tags=["Upload images"]
)


@router.post("/hotels")
async def add_image(name:int, file: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    procces_picture.delay(im_path)

