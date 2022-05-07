"""
redis客户端Manager
"""
import asyncio
import functools
import pickle

from awaits.awaitable import awaitable
from redis import ConnectionPool, StrictRedis
from rediscluster import RedisCluster, ClusterConnectionPool

from app.excpetions.RedisException import RedisException
from config import Config


class PityRedisManager(object):
    """非线程安全，可能存在问题
    """
    _cluster_pool = dict()
    _pool = dict()

    @property
    def client(self):
        pool = ConnectionPool(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB, max_connections=100,
                              password=Config.REDIS_PASSWORD,
                              decode_responses=True)
        return StrictRedis(connection_pool=pool, decode_responses=True)

    @staticmethod
    def delete_client(redis_id: int, cluster: bool):
        """
        根据redis_id和是否是集群删除客户端
        :param redis_id:
        :param cluster:
        :return:
        """
        if cluster:
            PityRedisManager._cluster_pool.pop(redis_id)
        else:
            PityRedisManager._pool.pop(redis_id)

    @staticmethod
    def get_cluster_client(redis_id: int, address: str):
        """
        获取redis集群客户端
        :param redis_id:
        :param address:
        :return:
        """
        cluster = PityRedisManager._cluster_pool.get(redis_id)
        if cluster is not None:
            return cluster
        client = PityRedisManager.get_cluster(address)
        PityRedisManager._cluster_pool[redis_id] = client
        return client

    @staticmethod
    def get_single_node_client(redis_id: int, address: str, password: str, db: int):
        """
        获取redis单实例客户端
        :param redis_id:
        :param address:
        :param password:
        :param db:
        :return:
        """
        node = PityRedisManager._pool.get(redis_id)
        if node is not None:
            return node
        host, port = address.split(":")
        pool = ConnectionPool(host=host, port=port, db=db, max_connections=100, password=password,
                              decode_responses=True)
        client = StrictRedis(connection_pool=pool)
        PityRedisManager._pool[redis_id] = client
        return client

    @staticmethod
    def refresh_redis_client(redis_id: int, address: str, password: str, db: str):
        """
        刷新redis客户端
        :param redis_id:
        :param address:
        :param password:
        :param db:
        :return:
        """
        host, port = address.split(":")
        pool = ConnectionPool(host=host, port=port, db=db, max_connections=100, password=password,
                              decode_responses=True)
        client = StrictRedis(connection_pool=pool, decode_responses=True)
        PityRedisManager._pool[redis_id] = client

    @staticmethod
    def refresh_redis_cluster(redis_id: int, addr: str):
        PityRedisManager._cluster_pool[redis_id] = PityRedisManager.get_cluster(addr)

    @staticmethod
    def get_cluster(address: str):
        """
        获取集群连接池
        :param address:
        :return:
        """
        try:
            nodes = address.split(',')
            startup_nodes = [{"host": n.split(":")[0], "port": n.split(":")[1]} for n in nodes]
            pool = ClusterConnectionPool(startup_nodes=startup_nodes, max_connections=100, decode_responses=True)
            client = RedisCluster(connection_pool=pool, decode_responses=True)
            return client
        except Exception as e:
            raise RedisException(f"获取Redis连接失败, {e}")


class RedisHelper(object):
    pity_prefix = "pity"
    pity_redis_client = PityRedisManager().client

    @staticmethod
    @awaitable
    def execute_command(client, command, *args, **kwargs):
        return client.execute_command(command, *args, **kwargs)

    @staticmethod
    @awaitable
    def ping():
        """
        test redis client
        :return:
        """
        return RedisHelper.pity_redis_client.ping()

    @staticmethod
    def get_key(key: str, args_key: bool = True, *args):
        if args_key:
            return f"{RedisHelper.pity_prefix}:{key}{':'.join(str(a) for a in args)}"
        return f"{RedisHelper.pity_prefix}:{key}"

    @staticmethod
    def cache(key: str, expired_time=3 * 60, args_key=True):
        """
        自动缓存装饰器
        :param args_key:
        :param key: 被缓存的key
        :param expired_time: 默认key过期时间
        :return:
        """

        def decorator(func):
            # 缓存已存在
            if asyncio.iscoroutinefunction(func):
                @functools.wraps(func)
                async def wrapper(*args, **kwargs):
                    redis_key = RedisHelper.get_key(key, args_key, *args)
                    data = RedisHelper.pity_redis_client.get(redis_key)
                    # 缓存已存在
                    if data is not None:
                        return pickle.loads(bytes.fromhex(data))
                    # 获取最新数据
                    new_data = await func(*args, **kwargs)
                    info = pickle.dumps(new_data)
                    RedisHelper.pity_redis_client.set(redis_key, info.hex(), ex=expired_time)
                    return new_data

                return wrapper
            else:
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    redis_key = RedisHelper.get_key(key, *args)
                    data = RedisHelper.pity_redis_client.get(redis_key)
                    # 缓存已存在
                    if data is not None:
                        return pickle.loads(bytes.fromhex(data))
                    # 获取最新数据
                    new_data = func(*args, **kwargs)
                    info = pickle.dumps(new_data)
                    RedisHelper.pity_redis_client.set(redis_key, info.hex(), ex=expired_time)
                    return new_data

                return wrapper

        return decorator

    @staticmethod
    def up_cache(key: str):
        """
        redis缓存key，套了此方法，会自动执行更新数据操作后删除缓存
        :param key:
        :return:
        """

        def decorator(func):
            redis_key = RedisHelper.get_key(key)
            if asyncio.iscoroutinefunction(func):
                @functools.wraps(func)
                async def wrapper(*args, **kwargs):
                    RedisHelper.pity_redis_client.delete(redis_key)
                    new_data = await func(*args, **kwargs)
                    # 更新数据，删除缓存
                    return new_data

                return wrapper
            else:

                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    new_data = func(*args, **kwargs)
                    RedisHelper.pity_redis_client.delete(redis_key)
                    return new_data

                return wrapper

        return decorator
