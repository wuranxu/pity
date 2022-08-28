import asyncio
import time
from concurrent import futures
from threading import Thread

import grpc

from app.utils.etcd import EtcdClient
from app.utils.register import ServiceRegister
from app.v1.user.api.UserService import UserServiceApi
from app.v1.user.proto import user_pb2_grpc

cfg = ServiceRegister.parse_config("./service.yml")
host, port = cfg.get("etcd").split(":")
service = cfg.get("service")
etcd = EtcdClient(host, port)
MAX_MESSAGE_LENGTH = 205109840


async def listen(instance, port):
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10),
                             options=[
                                 ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                                 ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
                             ])
    user_pb2_grpc.add_userServicer_to_server(instance, server)
    server.add_insecure_port('[::]{}'.format(port))
    print("服务启动成功, 端口: ", port)
    await server.start()
    await server.wait_for_termination()


def wait(timeout):
    while True:
        time.sleep(timeout)


def listen_server(instance, port):
    asyncio.run(listen(instance, port))


def serve(cfg, instance, port):
    etcd.register_api(service, instance, cfg)
    etcd.register_service(service, ServiceRegister.get_ip_address() + port, 10)


def main(cfg):
    port = ":{}".format(cfg.get("port"))
    instance = UserServiceApi()
    server = Thread(target=serve, args=(cfg, instance, port))
    lis = Thread(target=listen_server, args=(instance, port))
    server.start()
    lis.start()
    server.join()
    lis.join()


def term_sig_handler(lp):
    etcd.unregister_service(service, ServiceRegister.get_ip_address() + port).send(None)
    lp.stop()


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.add_signal_handler(signal.SIGTERM, term_sig_handler, loop)
    # loop.add_signal_handler(signal.SIGINT, term_sig_handler, loop)
    # loop.run_until_complete(main(cfg, port))
    main(cfg)
