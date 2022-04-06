from fastapi import Depends

from app.crud.config.GConfigDao import GConfigDao
from app.handler.fatcory import PityResponse
from app.routers import Permission
from app.routers.config.environment import router
from app.schema.gconfig import GConfigForm
from config import Config


@router.get("/gconfig/list")
async def list_gconfig(page: int = 1, size: int = 8, env: int = None, key: str = "", user_info=Depends(Permission())):
    data, total, err = GConfigDao.list_gconfig(page, size, env, key)
    if err:
        return PityResponse.failed(err)
    return PityResponse.success_with_size(code=0, data=data, total=total, msg="操作成功")


@router.post("/gconfig/insert")
async def insert_gconfig(data: GConfigForm, user_info=Depends(Permission(Config.ADMIN))):
    err = GConfigDao.insert_gconfig(data, user_info['id'])
    if err:
        return PityResponse.failed(err)
    return PityResponse.success()


@router.post("/gconfig/update")
async def update_gconfig(data: GConfigForm, user_info=Depends(Permission(Config.ADMIN))):
    err = GConfigDao.update_gconfig(data, user_info['id'])
    if err:
        return PityResponse.failed(err)
    return PityResponse.success()


@router.get("/gconfig/delete")
async def delete_gconfig(id: int, user_info=Depends(Permission(Config.ADMIN))):
    err = GConfigDao.delete_gconfig(id, user_info['id'])
    if err:
        return PityResponse.failed(err)
    return PityResponse.success()
