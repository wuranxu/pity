"""
grpc客户端，根据方法/参数请求grpc接口
"""
import asyncio

from grpc_requests import AsyncClient


class GrpcClient(object):
    """
    usage:
    result = GrpcClient.invoke("localhost:50001", "hello", "greeter", {"name": "woody"})
    print(result)
    """

    @staticmethod
    async def invoke(address: str, iface: str, method: str, request_data=None):
        client = AsyncClient(address)
        service = await client.service(iface)
        return await getattr(service, method)(request_data)


if __name__ == "__main__":
    asyncio.run(GrpcClient.invoke("localhost:50052", "Hello", "Edit", {"number": 10}))
