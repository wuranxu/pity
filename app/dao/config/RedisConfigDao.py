from app.dao import Mapper
from app.middleware.RedisManager import PityRedisManager
from app.models.redis_config import PityRedis
from app.utils.decorator import dao
from app.utils.logger import Log


@dao(PityRedis, Log("PityRedisConfigDao"))
class PityRedisConfigDao(Mapper):

    @staticmethod
    async def execute_command(command: str, **kwargs):
        redis_config = await PityRedisConfigDao.query_record(**kwargs)
        if not redis_config.cluster:
            client = PityRedisManager.get_single_node_client(redis_config.id, redis_config.addr,
                                                             redis_config.password, redis_config.db)
        else:
            client = PityRedisManager.get_cluster_client(redis_config.id, redis_config.addr)
        return client.execute_command(command)
