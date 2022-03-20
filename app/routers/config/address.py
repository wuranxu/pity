from fastapi import Depends

from app.crud.config.AddressDao import PityGatewayDao
from app.handler.fatcory import PityResponse
from app.models.address import PityGateway
from app.routers import Permission, get_session
from app.routers.config.environment import router
from app.schema.address import PityAddressForm
from config import Config


@router.get("/gateway/list")
async def list_gateway(name: str = '', gateway: str = '', env: int = None,
                       user_info=Depends(Permission(Config.MEMBER))):
    data = await PityGatewayDao.list_record(env=env, gateway=f"%{gateway}%", name=f"%{name}%")
    return PityResponse.success(PityResponse.model_to_list(data))


@router.post("/gateway/insert")
async def insert_gateway(form: PityAddressForm, user_info=Depends(Permission(Config.MANAGER))):
    model = PityGateway(**form.dict(), user=user_info['id'])
    model = await PityGatewayDao.insert_record(model, True)
    return PityResponse.success(model)


@router.post("/gateway/update")
async def insert_gateway(form: PityAddressForm, user_info=Depends(Permission(Config.MANAGER))):
    model = await PityGatewayDao.update_record_by_id(user_info['id'], form, True, log=True)
    return PityResponse.success(model)


@router.get("/gateway/delete")
async def delete_gateway(id: int, user_info=Depends(Permission(Config.MANAGER)), session=Depends(get_session)):
    await PityGatewayDao.delete_record_by_id(session, user_info['id'], id)
    return PityResponse.success()
