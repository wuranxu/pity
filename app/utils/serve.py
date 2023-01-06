"""rpc service 注册类
"""
from concurrent import futures
from typing import Callable

import grpc
from grpc_reflection.v1alpha import reflection
from loguru import logger

from app.exception.error import RpcError
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
        host = cfg.get("etcd")
        service = cfg.get("service")
        service_port = cfg.get("port")
        etcd = EtcdClient(host)
        await RpcService.register_service(client=etcd,
                                          service=service,
                                          instance=instance,
                                          cfg=cfg,
                                          port=f":{service_port}")

    @staticmethod
    def load_service_config(config: str):
        return ServiceRegister.parse_config(config)

    @staticmethod
    async def listen(service: str, port: int, register, instance, pb):
        """
        启动pity rpc服务
        :param service:
        :param instance:
        :param port:
        :param register:
        :return:
        """
        grpc.aio.init_grpc_aio()
        server = grpc.aio.server(
            migration_thread_pool=futures.ThreadPoolExecutor(max_workers=500),
            options=[
                ('grpc.max_send_message_length', RpcService.MAX_MESSAGE_LENGTH),
                ('grpc.max_receive_message_length', RpcService.MAX_MESSAGE_LENGTH),
            ])
        logger.info("开始注册服务到etcd. 👏")
        register(instance, server)
        SERVICE_NAMES = (
            pb.DESCRIPTOR.services_by_name[service].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, server)
        server.add_insecure_port('[::]:{}'.format(port))
        logger.info(f"服务启动成功, 端口: {port}. 🎉")
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
    async def start(config: str, dispatch: Callable, instance, pb):
        cfg = RpcService.load_service_config(config)
        logger.info("服务配置加载成功. ✔")
        port = cfg.get("port")
        service = cfg.get("service")
        if port is None:
            raise RpcError("请指定端口号, 不建议随机端口")
        await RpcService.register(instance, cfg)
        await RpcService.listen(service, port, dispatch, instance, pb)

    @staticmethod
    async def shutdown(cfg_file="./service.yml"):
        cfg = RpcService.load_service_config(cfg_file)
        etcd = EtcdClient(cfg.get("etcd"))
        service = cfg.get("service")
        addr = f"{ServiceRegister.get_ip_address()}:{cfg.get('port')}"
        await RpcService.unregister(client=etcd, service=service, cfg=cfg, addr=addr)

    @staticmethod
    async def register_service(*, client, service, instance, cfg, port):
        await client.register_api(service, instance, cfg)
        await client.register_service(service, ServiceRegister.get_ip_address() + port, 300)

    @staticmethod
    async def unregister(*, client, service, cfg, addr):
        await client.unregister_service(service, addr)
        await client.unregister_methods(service, cfg)
