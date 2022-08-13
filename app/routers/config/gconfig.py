from fastapi import Depends

from app.crud.config.GConfigDao import GConfigDao
from app.handler.fatcory import PityResponse
from app.routers import Permission, get_session
from app.routers.config.environment import router
from app.schema.gconfig import GConfigForm
from config import Config


@router.get("/gconfig/list")
async def list_gconfig(page: int = 1, size: int = 8, env=None, key: str = "", _=Depends(Permission())):
    data, total = await GConfigDao.list_with_pagination(page, size, env=env, key=key)
    return PityResponse.success_with_size(data=data, total=total)


@router.post("/gconfig/insert")
async def insert_gconfig(data: GConfigForm, user_info=Depends(Permission(Config.ADMIN))):
    await GConfigDao.insert_gconfig(data, user_info['id'])
    return PityResponse.success()


@router.post("/gconfig/update")
async def update_gconfig(data: GConfigForm, user_info=Depends(Permission(Config.ADMIN))):
    await GConfigDao.update_record_by_id(user_info['id'], data, True, True)
    return PityResponse.success()


@router.get("/gconfig/delete")
async def delete_gconfig(id: int, user_info=Depends(Permission(Config.ADMIN)), session=Depends(get_session)):
    await GConfigDao.delete_record_by_id(session, user_info['id'], id, log=True)
    return PityResponse.success()
