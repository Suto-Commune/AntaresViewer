import fastapi
import src.function.format.avi as AVI

router = fastapi.APIRouter()
Name = AVI.Name()
default_url = "/"


@router.get(default_url)
async def welcome():
    return {"text": "Welcome to AntaresViewer!"}
