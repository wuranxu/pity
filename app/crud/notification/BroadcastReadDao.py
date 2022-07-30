from app.crud import Mapper, ModelWrapper
from app.models.broadcast_read_user import PityBroadcastReadUser
from app.utils.logger import Log


@ModelWrapper(PityBroadcastReadUser, Log("BroadcastReadDao"))
class BroadcastReadDao(Mapper):
    pass
