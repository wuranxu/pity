from fastapi import APIRouter, Depends

from app.crud.config.EnvironmentDao import EnvironmentDao
from app.handler.fatcory import PityResponse
from app.routers import Permission
from app.schema.environment import EnvironmentForm
from config import Config

router = APIRouter(prefix="/config")


@router.get("/environment/list")
async def list_environment(page: int = 1, size: int = 8, name: str = "", exactly=False,
                           user_info=Depends(Permission())):
    data, total, err = EnvironmentDao.list_env(page, size, name, exactly)
    if err:
        return PityResponse.failed(code=110, msg=err)
    return PityResponse.success_with_size(code=0, data=data, total=total, msg="操作成功")


@router.post("/environment/insert")
async def insert_environment(data: EnvironmentForm, user_info=Depends(Permission(Config.ADMIN))):
    err = EnvironmentDao.insert_env(data, user_info['id'])
    if err:
        return PityResponse.failed(code=110, msg=err)
    return PityResponse.success()


@router.post("/environment/update")
async def update_environment(data: EnvironmentForm, user_info=Depends(Permission(Config.ADMIN))):
    err = EnvironmentDao.update_env(data, user_info['id'])
    if err:
        return PityResponse.failed(code=110, msg=err)
    return PityResponse.success()


@router.get("/environment/delete")
async def delete_environment(id: int, user_info=Depends(Permission(Config.ADMIN))):
    err = EnvironmentDao.delete_env(id, user_info['id'])
    if err:
        return PityResponse.failed(code=110, msg=err)
    return PityResponse.success()
