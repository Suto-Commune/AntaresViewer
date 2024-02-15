import fastapi

router = fastapi.APIRouter()
default_url = '/'+str(__name__).replace("src.server.event.", "").replace(".", "/")

print(str(default_url))


@router.get(default_url)
async def example():
    print(str(default_url))
    return {"Hello,AntaresViewer"}
