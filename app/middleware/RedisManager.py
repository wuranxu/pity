"""
redis客户端Manager
"""
import asyncio
import functools
import inspect
import json
import pickle
from random import Random
from typing import Tuple

from awaits.awaitable import awaitable
from loguru import logger
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
        if ":" not in address:
            raise Exception("redis连接未包含端口号，请检查配置")
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
            startup_nodes = [{"host": n.split(":")[0], "port": n.split(":")[1]} for n in nodes if ":" in n]
            if len(startup_nodes) == 0:
                raise Exception("找不到集群节点，请检查配置")
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
    @awaitable
    def get_address_record(address: str):
        """
        获取ip是否已经开启录制
        :param address:
        :return:
        """
        key = RedisHelper.get_key(f"record:ip:{address}")
        return RedisHelper.pity_redis_client.get(key)

    @staticmethod
    @awaitable
    def cache_record(address: str, request):
        """
        :param address:
        :param request:
        :return:
        """
        key = RedisHelper.get_key(f"record:{address}:requests")
        RedisHelper.pity_redis_client.rpush(key, request)
        ttl = RedisHelper.pity_redis_client.ttl(key)
        if ttl < 0:
            RedisHelper.pity_redis_client.expire(key, 3600)

    @staticmethod
    @awaitable
    def set_address_record(user_id: int, address: str, regex: str):
        """
        设置录制状态
        :param user_id:
        :param address:
        :param regex: 录制的url正则
        :return:
        """
        # 默认录制1小时
        value = json.dumps({"user_id": user_id, "regex": regex}, ensure_ascii=False)
        RedisHelper.pity_redis_client.set(RedisHelper.get_key(f"record:ip:{address}"), value, ex=3600)
        # 清除上次录制数据
        RedisHelper.pity_redis_client.delete(RedisHelper.get_key(f"record:{address}:requests"))

    @staticmethod
    @awaitable
    def remove_address_record(address: str):
        """
        停止录制任务
        :param address:
        :return:
        """
        return RedisHelper.pity_redis_client.delete(RedisHelper.get_key(f"record:ip:{address}"))

    @staticmethod
    @awaitable
    def list_record_data(address: str):
        """
        获取录制数据
        :param address:
        :return:
        """
        key = RedisHelper.get_key(f"record:{address}:requests")
        data = RedisHelper.pity_redis_client.lrange(key, 0, -1)
        return [json.loads(x) for x in data]

    @staticmethod
    @awaitable
    def remove_record_data(address: str, index: int):
        """
        停止录制任务
        :param address:
        :param index:
        :return:
        """
        key = RedisHelper.get_key(f"record:{address}:requests")
        RedisHelper.pity_redis_client.lset(key, index, "DELETED")
        RedisHelper.pity_redis_client.lrem(key, 1, "DELETED")

    @staticmethod
    @awaitable
    def async_delete_prefix(key: str):
        """
        根据前缀删除数据
        :param key:
        :return:
        """
        for k in RedisHelper.pity_redis_client.scan_iter(f"{key}*"):
            RedisHelper.pity_redis_client.delete(k)
            logger.bind(name=None).debug(f"delete redis key: {k}")

    @staticmethod
    def delete_prefix(key: str):
        """
        根据前缀删除数据
        :param key:
        :return:
        """
        for k in RedisHelper.pity_redis_client.scan_iter(f"{key}*"):
            RedisHelper.pity_redis_client.delete(k)
            logger.bind(name=None).debug(f"delete redis key: {k}")

    @staticmethod
    def get_key(_redis_key: str, args_key: bool = True, *args, **kwargs):
        if not args_key:
            return f"{RedisHelper.pity_prefix}:{_redis_key}"
        filter_args = [a for a in args if not str(a).startswith(('<class', '<sqlalchemy', '(<sqlalchemy'))]
        for v in kwargs.values():
            if v and not str(v).startswith(('<class', '<sqlalchemy', '(<sqlalchemy')):
                filter_args.append(str(v))
        return f"{RedisHelper.pity_prefix}:{_redis_key}" \
               f"{':' + ':'.join(str(a) for a in filter_args) if len(filter_args) > 0 else ''}"

    @staticmethod
    def get_key_with_suffix(cls_name: str, key: str, args: tuple, key_suffix):
        filter_args = [a for a in args if not str(args[0]).startswith('<class')]
        suffix = key_suffix(filter_args)
        return f"{RedisHelper.pity_prefix}:{cls_name}:{key}:{suffix}"

    @staticmethod
    def cache(key: str, expired_time=30 * 60, args_key=True):
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
                    if not Config.REDIS_ON:
                        return await func(*args, **kwargs)
                    cls_name = inspect.getframeinfo(inspect.currentframe().f_back)[3][0].split(".")[0].split(" ")[-1]
                    redis_key = RedisHelper.get_key(f"{cls_name}:{key}", args_key, *args, **kwargs)
                    data = RedisHelper.pity_redis_client.get(redis_key)
                    # 缓存已存在
                    if data is not None:
                        return pickle.loads(bytes.fromhex(data))
                    # 获取最新数据
                    new_data = await func(*args, **kwargs)
                    info = pickle.dumps(new_data)
                    # logger.bind(name=None).debug(f"set redis key: {redis_key}")
                    RedisHelper.pity_redis_client.set(redis_key, info.hex(), ex=expired_time)
                    return new_data

                return wrapper
            else:
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    if not Config.REDIS_ON:
                        return func(*args, **kwargs)
                    cls_name = inspect.getframeinfo(inspect.currentframe().f_back)[3][0].split(".")[0].split(" ")[-1]
                    redis_key = RedisHelper.get_key(f"{cls_name}:{key}", args_key, *args, **kwargs)
                    data = RedisHelper.pity_redis_client.get(redis_key)
                    # 缓存已存在
                    if data is not None:
                        return pickle.loads(bytes.fromhex(data))
                    # 获取最新数据
                    new_data = func(*args, **kwargs)
                    info = pickle.dumps(new_data)
                    # logger.bind(name=None).debug(f"set redis key: {redis_key}")
                    # 添加随机数防止缓存雪崩
                    RedisHelper.pity_redis_client.set(redis_key, info.hex(), ex=expired_time + Random().randint(10, 59))
                    return new_data

                return wrapper

        return decorator

    @staticmethod
    def up_cache(*key: str, key_and_suffix: Tuple = None):
        """
        redis缓存key，套了此方法，会自动执行更新数据操作后删除缓存
        :param key:
        :param key_and_suffix: 要删除的key和key组成规则
        :return:
        """

        def decorator(func):
            if asyncio.iscoroutinefunction(func):
                @functools.wraps(func)
                async def wrapper(*args, **kwargs):
                    new_data = await func(*args, **kwargs)
                    if not Config.REDIS_ON:
                        return new_data
                    cls_name = inspect.getframeinfo(inspect.currentframe().f_back)[3][0].split(".")[0].split(" ")[-1]
                    for k in key:
                        redis_key = f"{RedisHelper.pity_prefix}:{cls_name}:{k}"
                        await RedisHelper.async_delete_prefix(redis_key)
                    if key_and_suffix is not None:
                        current_key = RedisHelper.get_key_with_suffix(cls_name, key_and_suffix[0], args,
                                                                      key_and_suffix[1])
                        RedisHelper.pity_redis_client.delete(current_key)
                    # 更新数据，删除缓存
                    return new_data

                return wrapper
            else:
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    new_data = func(*args, **kwargs)
                    if not Config.REDIS_ON:
                        return new_data
                    cls_name = inspect.getframeinfo(inspect.currentframe().f_back)[3][0].split(".")[0].split(" ")[-1]
                    for k in key:
                        redis_key = f"{RedisHelper.pity_prefix}:{cls_name}:{k}"
                        RedisHelper.delete_prefix(redis_key)
                    if key_and_suffix is not None:
                        current_key = RedisHelper.get_key_with_suffix(cls_name, key_and_suffix[0], args,
                                                                      key_and_suffix[1])
                        RedisHelper.pity_redis_client.delete(current_key)
                    return new_data

                return wrapper

        return decorator
