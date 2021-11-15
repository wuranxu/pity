"""
redis客户端Manager
"""
from redis import ConnectionPool, StrictRedis
from rediscluster import RedisCluster, ClusterConnectionPool

from app.excpetions.RedisException import RedisException


class PityRedisManager(object):
    """非线程安全，可能存在问题
    """
    _cluster_pool = dict()
    _pool = dict()

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
    def get_cluster_client(redis_id: int, addr: str):
        """
        获取redis集群客户端
        :param redis_id:
        :param addr:
        :return:
        """
        cluster = PityRedisManager._cluster_pool.get(redis_id)
        if cluster is not None:
            return cluster
        client = PityRedisManager.get_cluster(addr)
        PityRedisManager._cluster_pool[redis_id] = client
        return client

    @staticmethod
    def get_single_node_client(redis_id: int, addr: str, password: str, db: int):
        """
        获取redis单实例客户端
        :param redis_id:
        :param addr:
        :param password:
        :param db:
        :return:
        """
        node = PityRedisManager._pool.get(redis_id)
        if node is not None:
            return node
        host, port = addr.split(":")
        pool = ConnectionPool(host=host, port=port, db=db, max_connections=100, password=password,
                              decode_responses=True)
        client = StrictRedis(connection_pool=pool)
        PityRedisManager._pool[redis_id] = client
        return client

    @staticmethod
    def refresh_redis_client(redis_id: int, addr: str, password: str, db: str):
        """
        刷新redis客户端
        :param redis_id:
        :param addr:
        :param password:
        :param db:
        :return:
        """
        host, port = addr.split(":")
        pool = ConnectionPool(host=host, port=port, db=db, max_connections=100, password=password,
                              decode_responses=True)
        client = StrictRedis(connection_pool=pool, decode_responses=True)
        PityRedisManager._pool[redis_id] = client

    @staticmethod
    def refresh_redis_cluster(redis_id: int, addr: str):
        PityRedisManager._cluster_pool[redis_id] = PityRedisManager.get_cluster(addr)

    @staticmethod
    def get_cluster(addr: str):
        """
        获取集群连接池
        :param addr:
        :return:
        """
        try:
            nodes = addr.split(',')
            startup_nodes = [{"host": n.split(":")[0], "port": n.split(":")[1]} for n in nodes]
            pool = ClusterConnectionPool(startup_nodes=startup_nodes, max_connections=100, decode_responses=True)
            client = RedisCluster(connection_pool=pool, decode_responses=True)
            return client
        except Exception as e:
            raise RedisException(f"获取Redis连接失败, {e}")
