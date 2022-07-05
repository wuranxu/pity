import asyncio
from mimetypes import guess_type
from os.path import isfile

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Request, WebSocket, WebSocketDisconnect, Depends
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app import pity, init_logging
from app.core.msg.wss_msg import WebSocketMessage
from app.core.ws_connection_manager import ws_manage
from app.crud import create_table
from app.crud.notification.NotificationDao import PityNotificationDao
from app.enums.MessageEnum import MessageStateEnum, MessageTypeEnum
from app.middleware.RedisManager import RedisHelper
from app.routers.auth import user
from app.routers.config import router as config_router
from app.routers.notification import router as msg_router
from app.routers.online import router as online_router
from app.routers.operation import router as operation_router
from app.routers.oss import router as oss_router
from app.routers.project import project
from app.routers.request import http
from app.routers.testcase import router as testcase_router
from app.routers.workspace import router as workspace_router
from app.utils.scheduler import Scheduler
from config import Config, PITY_ENV, BANNER

logger = init_logging()

logger.bind(name=None).opt(ansi=True).success(f"pity is running at <red>{PITY_ENV}</red>")
logger.bind(name=None).success(BANNER)


async def request_info(request: Request):
    logger.bind(name=None).debug(f"{request.method} {request.url}")
    try:
        body = await request.json()
        logger.bind(payload=body, name=None).debug("request_json: ")
    except:
        try:
            body = await request.body()
            if len(body) != 0:
                # 有请求体，记录日志
                logger.bind(payload=body, name=None).debug(body)
        except:
            # 忽略文件上传类型的数据
            pass


# 注册路由
pity.include_router(user.router)
pity.include_router(project.router, dependencies=[Depends(request_info)])
pity.include_router(http.router, dependencies=[Depends(request_info)])
pity.include_router(testcase_router, dependencies=[Depends(request_info)])
pity.include_router(config_router, dependencies=[Depends(request_info)])
pity.include_router(online_router, dependencies=[Depends(request_info)])
pity.include_router(oss_router, dependencies=[Depends(request_info)])
pity.include_router(operation_router, dependencies=[Depends(request_info)])
pity.include_router(msg_router, dependencies=[Depends(request_info)])
pity.include_router(workspace_router, dependencies=[Depends(request_info)])

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
async def get_site_static(filename):
    filename = './statics/static/' + filename

    if not isfile(filename):
        return Response(status_code=404)

    with open(filename, mode='rb') as f:
        content = f.read()

    content_type, _ = guess_type(filename)
    return Response(content, media_type=content_type)


@pity.on_event('startup')
async def init_redis():
    """
    初始化redis，失败则服务起不来
    :return:
    """
    try:
        await RedisHelper.ping()
        logger.bind(name=None).success("redis connected success.        ✔")
    except Exception as e:
        if not Config.REDIS_ON:
            logger.bind(name=None).warning(
                f"Redis is not selected, So we can't ensure that the task is not executed repeatedly.        🚫")
            return
        logger.bind(name=None).error(f"Redis connect failed, Please check config.py for redis config.        ❌")
        raise e


@pity.on_event('startup')
def init_scheduler():
    """
    初始化定时任务
    :return:
    """
    # SQLAlchemyJobStore指定存储链接
    job_store = {
        'default': SQLAlchemyJobStore(url=Config.SQLALCHEMY_DATABASE_URI, engine_options={"pool_recycle": 1500},
                                      pickle_protocol=3)
    }
    scheduler = AsyncIOScheduler()
    Scheduler.init(scheduler)
    Scheduler.configure(jobstores=job_store)
    Scheduler.start()
    logger.bind(name=None).success("ApScheduler started success.        ✔")


@pity.on_event('startup')
async def init_database():
    """
    初始化数据库，建表
    :return:
    """
    try:
        asyncio.create_task(create_table())
        logger.bind(name=None).success("database and tables created success.        ✔")
    except Exception as e:
        logger.bind(name=None).error(f"database and tables  created failed.        ❌\nerror: {e}")
        raise


@pity.on_event('shutdown')
def stop_test():
    pass


@pity.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    async def send_heartbeat():
        while True:
            logger.debug("sending heartbeat")
            await websocket.send_json({
                'type': 3
            })
            await asyncio.sleep(Config.HEARTBEAT)

    await ws_manage.connect(websocket, user_id)
    try:
        # 定义特殊值的回复，配合前端实现确定连接，心跳检测等逻辑
        questions_and_answers_map: dict = {
            "HELLO SERVER": F"hello {user_id}",
            "HEARTBEAT": F"{user_id}",
        }

        # 存储连接后获取消息
        msg_records = await PityNotificationDao.list_messages(msg_type=MessageTypeEnum.all.value, receiver=user_id,
                                                              msg_status=MessageStateEnum.unread.value)
        # 如果有未读消息, 则推送给前端对应的count
        if len(msg_records) > 0:
            await websocket.send_json(WebSocketMessage.msg_count(len(msg_records), True))
        # 发送心跳包
        # asyncio.create_task(send_heartbeat())
        while True:
            data: str = await websocket.receive_text()
            du = data.upper()
            if du in questions_and_answers_map:
                await ws_manage.send_personal_message(message=questions_and_answers_map.get(du), websocket=websocket)
    except WebSocketDisconnect:
        if user_id in ws_manage.active_connections:
            ws_manage.disconnect(user_id)
    except Exception as e:
        logger.bind(name=None).debug(f"websocket: 用户: {user_id} 异常退出: {e}")
