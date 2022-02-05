from app.crud import Mapper
from app.models.broadcast_read_user import PityBroadcastReadUser
from app.utils.decorator import dao
from app.utils.logger import Log


@dao(PityBroadcastReadUser, Log("BroadcastReadDao"))
class BroadcastReadDao(Mapper):
    pass
