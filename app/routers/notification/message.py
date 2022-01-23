from typing import List

from fastapi import APIRouter, Depends

from app.crud.notification.NotificationDao import PityNotificationDao
from app.handler.fatcory import PityResponse
from app.models.notification import PityNotification
from app.routers import Permission

router = APIRouter(prefix="/notification")


@router.get("/list", description="获取用户消息列表")
async def list_msg(msg_status: int = 0, msg_type: int = 0, user_info=Depends(Permission())):
    try:
        data = await PityNotificationDao.list_record(msg_type=msg_type, msg_status=msg_status,
                                                     receiver=user_info['id'])
        return PityResponse.success(data)
    except Exception as e:
        return PityResponse.failed(str(e))


@router.post("/read", description="用户读取消息")
async def read_msg(msg_id: List[int], user_info=Depends(Permission())):
    try:
        await PityNotificationDao.update_by_map(PityNotification.id.in_(msg_id),
                                                PityNotification.receiver == user_info['id'], msg_status=1)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(str(e))
