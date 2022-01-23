from app.crud import Mapper
from app.models.notification import PityNotification
from app.utils.decorator import dao
from app.utils.logger import Log


@dao(PityNotification, Log("PityNotificationDao"))
class PityNotificationDao(Mapper):
    pass
