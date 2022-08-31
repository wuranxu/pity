import asyncio

from app.utils.serve import RpcService
from app.v1.user.api.UserService import UserServiceApi
from app.v1.user.proto import user_pb2_grpc


async def main():
    await RpcService.start("./service.yml", user_pb2_grpc.add_userServicer_to_server, UserServiceApi())


if __name__ == "__main__":
    asyncio.run(main())
