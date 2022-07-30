from app.crud import Mapper, ModelWrapper
from app.middleware.RedisManager import PityRedisManager, RedisHelper
from app.models.redis_config import PityRedis


@ModelWrapper(PityRedis)
class PityRedisConfigDao(Mapper):

    @staticmethod
    async def execute_command(command: str, **kwargs):
        try:
            redis_config = await PityRedisConfigDao.query_record(**kwargs)
            if redis_config is None:
                raise Exception("Redis配置不存在")
            if not redis_config.cluster:
                client = PityRedisManager.get_single_node_client(redis_config.id, redis_config.addr,
                                                                 redis_config.password, redis_config.db)
            else:
                client = PityRedisManager.get_cluster_client(redis_config.id, redis_config.addr)
            return await RedisHelper.execute_command(client, command)
        except Exception as e:
            raise Exception(f"执行redis命令出错: {e}")
