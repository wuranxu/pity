from fastapi import Depends

from app.core.configuration import SystemConfiguration
from app.handler.fatcory import PityResponse
from app.routers import Permission
from app.routers.config.gconfig import router
from config import Config


@router.get("/system", description="获取系统配置")
def get_system_config(_=Depends(Permission(Config.ADMIN))):
    configuration = SystemConfiguration.get_config()
    return PityResponse.success(configuration)


@router.post("/system/update", description="更新系统配置")
def get_system_config(data: dict, _=Depends(Permission(Config.ADMIN))):
    SystemConfiguration.update_config(data)
    return PityResponse.success()
