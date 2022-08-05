from typing import List

from fastapi import APIRouter, Depends

from app.crud.notification.BroadcastReadDao import BroadcastReadDao
from app.crud.notification.NotificationDao import PityNotificationDao
from app.enums.MessageEnum import MessageStateEnum
from app.handler.fatcory import PityResponse
from app.models.broadcast_read_user import PityBroadcastReadUser
from app.models.notification import PityNotification
from app.schema.notification import NotificationForm
from app.routers import Permission, get_session

router = APIRouter(prefix="/notification")


@router.get("/list", description="获取用户消息列表")
async def list_msg(msg_status: int, msg_type: int, user_info=Depends(Permission())):
    try:
        data = await PityNotificationDao.list_messages(msg_type=msg_type, msg_status=msg_status,
                                                       receiver=user_info['id'])
        return PityResponse.success(data)
    except Exception as e:
        return PityResponse.failed(str(e))


@router.post("/read", description="用户读取消息")
async def read_msg(form: NotificationForm, user_info=Depends(Permission())):
    try:
        if form.personal:
            await PityNotificationDao.update_by_map(user_info['id'],
                                                    PityNotification.id.in_(form.personal),
                                                    PityNotification.receiver == user_info['id'],
                                                    msg_status=MessageStateEnum.read.value)
        if form.broadcast:
            user_id = user_info['id']
            for f in form.broadcast:
                model = PityBroadcastReadUser(f, user_id)
                await BroadcastReadDao.insert(model=model)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(str(e))


@router.post("/delete", description="用户删除消息")
async def read_msg(msg_id: List[int], user_info=Depends(Permission()), session=Depends(get_session)):
    try:
        await PityNotificationDao.delete_message(session, msg_id, user_info['id'])
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(str(e))
