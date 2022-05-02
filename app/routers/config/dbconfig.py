from fastapi import Depends

from app.crud.config.DbConfigDao import DbConfigDao
from app.handler.fatcory import PityResponse
from app.models import DatabaseHelper, db_helper
from app.routers import Permission
from app.routers.config.environment import router
from app.schema.database import DatabaseForm
from config import Config


@router.get("/dbconfig/list")
async def list_dbconfig(name: str = '', database: str = '', env: int = None,
                        user_info=Depends(Permission(Config.MEMBER))):
    try:
        data = await DbConfigDao.list_database(name, database, env)
        return PityResponse.success(data)
    except Exception as err:
        return PityResponse.failed(err)


@router.post("/dbconfig/insert")
async def insert_dbconfig(form: DatabaseForm, user_info=Depends(Permission(Config.ADMIN))):
    try:
        await DbConfigDao.insert_database(form, user_info['id'])
        return PityResponse.success()
    except Exception as err:
        return PityResponse.failed(err)


@router.post("/dbconfig/update")
async def update_dbconfig(form: DatabaseForm, user_info=Depends(Permission(Config.ADMIN))):
    try:
        await DbConfigDao.update_database(form, user_info['id'])
        return PityResponse.success()
    except Exception as err:
        return PityResponse.failed(err)


@router.get("/dbconfig/delete", summary="删除数据库配置")
async def delete_dbconfig(id: int, user_info=Depends(Permission(Config.ADMIN))):
    try:
        await DbConfigDao.delete_database(id, user_info['id'])
        return PityResponse.success()
    except Exception as err:
        return PityResponse.failed(err)


@router.get("/dbconfig/connect", summary="测试数据库连接")
async def connect_test(sql_type: int, host: str, port: int, username: str, password: str, database: str,
                       _=Depends(Permission(Config.MANAGER))):
    try:
        data = await db_helper.get_connection(sql_type, host, port, username, password, database)
        if data is None:
            raise Exception("测试连接失败")
        await DatabaseHelper.test_connection(data.get("session"))
        return PityResponse.success(msg="连接成功")
    except Exception as e:
        return PityResponse.failed(str(e))
