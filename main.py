import hashlib
from mimetypes import guess_type
from os.path import isfile

import uvicorn
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app import pity
from app.models.schema.wechat import WechatForm
from app.routers.auth import user
from app.routers.config import router as config_router
from app.routers.online import router as online_router
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


@pity.get("/wx")
async def wechat(data: WechatForm):
    try:
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = "pitywoodytestplatform619434176"  # 请按照公众平台官网\基本配置中信息填写
        ls = [token, timestamp, nonce]
        ls.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            return echostr
        else:
            return ""
    except Exception:
        return ''


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
                                      pickle_protocol=4)
    }
    scheduler = AsyncIOScheduler()
    Scheduler.init(scheduler)
    Scheduler.configure(jobstores=job_store)
    Scheduler.start()


if __name__ == "__main__":
    uvicorn.run(app='main:pity', host='0.0.0.0', port=7777, reload=False)
