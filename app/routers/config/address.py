from fastapi import Depends

from app.crud.config.AddressDao import PityGatewayDao
from app.handler.fatcory import PityResponse
from app.models.address import PityGateway
from app.routers import Permission, get_session
from app.routers.config.environment import router
from app.schema.address import PityAddressForm
from config import Config


@router.get("/gateway/list", summary="查询网关地址")
async def list_gateway(name: str = '', gateway: str = '', env: int = None, _=Depends(Permission(Config.MEMBER))):
    data = await PityGatewayDao.select_list(env=env, gateway=f"%{gateway}%", name=f"%{name}%")
    return PityResponse.success(data)


@router.post("/gateway/insert", summary="添加网关地址", description="添加网关地址，只有组长可以操作")
async def insert_gateway(form: PityAddressForm, user_info=Depends(Permission(Config.MANAGER))):
    model = PityGateway(**form.dict(), user_id=user_info['id'])
    model = await PityGatewayDao.insert(model=model, log=True)
    return PityResponse.success(model)


@router.post("/gateway/update", summary="编辑网关地址", description="编辑网关地址，只有组长可以操作")
async def update_gateway(form: PityAddressForm, user_info=Depends(Permission(Config.MANAGER))):
    model = await PityGatewayDao.update_record_by_id(user_info['id'], form, True, log=True)
    return PityResponse.success(model)


@router.get("/gateway/delete", summary="删除网关地址", description="根据id删除网关地址，只有组长可以操作")
async def delete_gateway(id: int, user_info=Depends(Permission(Config.MANAGER)), session=Depends(get_session)):
    await PityGatewayDao.delete_record_by_id(session, user_info['id'], id)
    return PityResponse.success()
