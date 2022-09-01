"""rpc service 注册类
"""
import asyncio
from concurrent import futures
from typing import Callable

import grpc

from app.excpetions.RpcError import RpcError
from app.utils.etcd import EtcdClient
from app.utils.register import ServiceRegister


class RpcService(object):
    MAX_MESSAGE_LENGTH = 205109840

    @staticmethod
    async def register(instance, cfg: dict):
        """

        :param cfg: 配置文件路径，默认为service.yml
        :param instance: grpc服务注册实例
        :return:
        """
        host, port = RpcService.get_etcd_host_port(cfg.get("etcd"))
        service = cfg.get("service")
        service_port = cfg.get("port")
        etcd = EtcdClient(host, port)
        await RpcService.register_service(client=etcd,
                                          service=service,
                                          instance=instance,
                                          cfg=cfg,
                                          port=f":{service_port}")

    @staticmethod
    def load_service_config(config: str):
        return ServiceRegister.parse_config(config)

    @staticmethod
    async def listen(port: int, register, instance):
        """
        启动pity rpc服务
        :param instance:
        :param port:
        :param register:
        :return:
        """
        server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=30),
                                 options=[
                                     ('grpc.max_send_message_length', RpcService.MAX_MESSAGE_LENGTH),
                                     ('grpc.max_receive_message_length', RpcService.MAX_MESSAGE_LENGTH),
                                 ])
        register(instance, server)
        server.add_insecure_port('[::]:{}'.format(port))
        print("服务启动成功, 端口: ", port)
        await server.start()
        await server.wait_for_termination()

    @staticmethod
    def get_etcd_host_port(addr: str) -> (str, str):
        """
        分解etcd地址
        :param addr:
        :return: host and port
        """
        if not addr:
            raise RpcError("etcd配置不能为空")
        return addr.split(":")

    @staticmethod
    async def thread_wrapper(instance, cfg):
        await asyncio.to_thread(RpcService.register(instance, cfg))

    @staticmethod
    async def start(config: str, dispatch: Callable, instance):
        cfg = RpcService.load_service_config(config)
        port = cfg.get("port")
        if port is None:
            raise RpcError("请指定端口号, 不建议随机端口")
        server = asyncio.create_task(RpcService.listen(port, dispatch, instance))
        register = asyncio.create_task(RpcService.register(instance, cfg))
        await asyncio.gather(server, register)

    @staticmethod
    async def register_service(*, client, service, instance, cfg, port):
        client.register_api(service, instance, cfg)
        await client.register_service(service, ServiceRegister.get_ip_address() + port, 10)
