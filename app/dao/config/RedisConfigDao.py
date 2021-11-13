from app.dao import Mapper
from app.models.redis_config import PityRedis
from app.utils.decorator import dao
from app.utils.logger import Log


@dao(PityRedis, Log("PityRedisConfigDao"))
class PityRedisConfigDao(Mapper):
    pass
