from fastapi import APIRouter, Depends

from app.crud.config.EnvironmentDao import EnvironmentDao
from app.handler.fatcory import PityResponse
from app.routers import Permission, get_session
from app.schema.environment import EnvironmentForm
from config import Config

router = APIRouter(prefix="/config")


@router.get("/environment/list")
async def list_environment(page: int = 1, size: int = 8, name: str = "", exactly=False,
                           user_info=Depends(Permission())):
    data, total = await EnvironmentDao.list_env(page, size, name, exactly)
    return PityResponse.success_with_size(data=data, total=total)


@router.post("/environment/insert")
async def insert_environment(data: EnvironmentForm, user_info=Depends(Permission(Config.ADMIN))):
    await EnvironmentDao.insert_env(data, user_info['id'])
    return PityResponse.success()


@router.post("/environment/update")
async def update_environment(data: EnvironmentForm, user_info=Depends(Permission(Config.ADMIN))):
    ans = await EnvironmentDao.update_record_by_id(user_info['id'], data, True, True)
    return PityResponse.success(ans)


@router.get("/environment/delete")
async def delete_environment(id: int, user_info=Depends(Permission(Config.ADMIN)), session=Depends(get_session)):
    await EnvironmentDao.delete_record_by_id(session, user_info['id'], id)
    return PityResponse.success()
