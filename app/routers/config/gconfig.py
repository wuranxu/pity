from fastapi import Depends

from app.dao.config.GConfigDao import GConfigDao
from app.handler.fatcory import PityResponse
from app.models.schema.gconfig import GConfigForm
from app.routers import Permission
from app.routers.config.environment import router
from config import Config


@router.get("/gconfig/list")
async def list_gconfig(page: int = 1, size: int = 8, env: int = None, key: str = "", user_info=Depends(Permission())):
    data, total, err = GConfigDao.list_gconfig(page, size, env, key)
    if err:
        return dict(code=110, msg=err)
    return dict(code=0, data=PityResponse.model_to_list(data), total=total, msg="操作成功")


@router.post("/gconfig/insert")
async def insert_gconfig(data: GConfigForm, user_info=Depends(Permission(Config.ADMIN))):
    err = GConfigDao.insert_gconfig(data, user_info['id'])
    if err:
        return dict(code=110, msg=err)
    return dict(code=0, msg="操作成功")


@router.post("/gconfig/update")
async def update_gconfig(data: GConfigForm, user_info=Depends(Permission(Config.ADMIN))):
    err = GConfigDao.update_gconfig(data, user_info['id'])
    if err:
        return dict(code=110, msg=err)
    return dict(code=0, msg="操作成功")


@router.get("/gconfig/delete")
async def delete_gconfig(id: int, user_info=Depends(Permission(Config.ADMIN))):
    err = GConfigDao.delete_gconfig(id, user_info['id'])
    if err:
        return dict(code=110, msg=err)
    return dict(code=0, msg="操作成功")
