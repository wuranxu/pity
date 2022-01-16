from mimetypes import guess_type
from os.path import isfile

import uvicorn
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app import pity
from app.core.ws_connection_manager import ConnectionManager
from app.routers.auth import user
from app.routers.config import router as config_router
from app.routers.online import router as online_router
from app.routers.operation import router as operation_router
from app.routers.oss import router as oss_router
from app.routers.project import project
from app.routers.request import http
from app.routers.testcase import router as testcase_router
from app.utils.scheduler import Scheduler
from config import Config

pity.include_router(user.router)
pity.include_router(project.router)
pity.include_router(http.router)
pity.include_router(testcase_router)
pity.include_router(config_router)
pity.include_router(online_router)
pity.include_router(oss_router)
pity.include_router(operation_router)

pity.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pity.mount("/statics", StaticFiles(directory="statics"), name="statics")

templates = Jinja2Templates(directory="statics")
ws_manage = ConnectionManager()


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
async def get_site_static(filename):
    filename = './statics/static/' + filename

    if not isfile(filename):
        return Response(status_code=404)

    with open(filename, mode='rb') as f:
        content = f.read()

    content_type, _ = guess_type(filename)
    return Response(content, media_type=content_type)


@pity.on_event('startup')
def init_scheduler():
    # SQLAlchemyJobStore指定存储链接
    job_store = {
        'default': SQLAlchemyJobStore(url=Config.SQLALCHEMY_DATABASE_URI, engine_options={"pool_recycle": 1500},
                                      pickle_protocol=3)
    }
    scheduler = AsyncIOScheduler()
    Scheduler.init(scheduler)
    Scheduler.configure(jobstores=job_store)
    Scheduler.start()


@pity.on_event('shutdown')
def stop_test():
    pass


@pity.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await ws_manage.connect(websocket, client_id)
    # 定义特殊值的回复，配合前端实现确定连接，心跳检测等逻辑
    questions_and_answers_map: dict = {
        "HELLO SERVER": F"hello {client_id}",
        "HEARTBEAT": F"{client_id}",
    }
    try:
        while True:
            data: str = await websocket.receive_text()
            if (du := data.upper()) in questions_and_answers_map:
                await ws_manage.send_personal_message(message=questions_and_answers_map.get(du), websocket=websocket)
    except WebSocketDisconnect:
        if client_id in ws_manage.active_connections:
            ws_manage.disconnect(client_id)


if __name__ == "__main__":
    uvicorn.run(app='main:pity', host='0.0.0.0', port=7777, reload=False)
