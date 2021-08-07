from mimetypes import guess_type
from os.path import isfile

import uvicorn
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app import pity
from app.routers.auth import user
from app.routers.config import router as config_router
from app.routers.project import project
from app.routers.request import http
from app.routers.testcase import testcase

pity.include_router(user.router)
pity.include_router(project.router)
pity.include_router(http.router)
pity.include_router(testcase.router)
pity.include_router(config_router)

pity.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pity.mount("/statics", StaticFiles(directory="statics"), name="statics")

templates = Jinja2Templates(directory="statics")


@pity.get("/")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@pity.get("/{filename}")
async def get_site(filename):
    filename = './statics/' + filename

    if not isfile(filename):
        return Response(status_code=404)

    with open(filename, mode='rb') as f:
        content = f.read()

    content_type, _ = guess_type(filename)
    return Response(content, media_type=content_type)


@pity.get("/static/{filename}")
async def get_site(filename):
    filename = './statics/static/' + filename

    if not isfile(filename):
        return Response(status_code=404)

    with open(filename, mode='rb') as f:
        content = f.read()

    content_type, _ = guess_type(filename)
    return Response(content, media_type=content_type)


if __name__ == "__main__":
    uvicorn.run(app='main:pity', host='0.0.0.0', port=7777, reload=False)
