import asyncio
import inspect
import sys
import time

from grpc import aio
from locust import task, FastHttpUser, events, constant

from app.v1.request_pb2 import Request
from proto.user_pb2_grpc import userStub


def stopwatch(func):
    async def wrapper(*args, **kwargs):

        previous_frame = inspect.currentframe().f_back
        _, _, task_name, _, _ = inspect.getframeinfo(previous_frame)
        start = time.time()
        result = None
        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            total = int((time.time() - start) * 1000)
            events.request_failure.fire(request_type="TYPE",
                                        name=task_name,
                                        response_time=total,
                                        response_length=0,
                                        exception=e)
        else:
            total = int((time.time() - start) * 1000)
            events.request_success.fire(request_type="TYPE",
                                        name=task_name,
                                        response_time=total,
                                        response_length=0)
        return result

    return wrapper


class GRPCMyLocust(FastHttpUser):
    host = 'http://127.0.0.1:10077'  # 服务端地址和端口号
    wait_time = constant(0)

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task
    @stopwatch
    async def grpc_client_task(self):
        try:  # 服务端地址和端口号
            async with aio.insecure_channel('localhost:10011') as channel:
                stub = userStub(channel)
                response = await stub.listUser(Request())
                if response.code != 0:
                    raise Exception("code not 0")
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)


if __name__ == "__main__":
    async def main():
        async with aio.insecure_channel('localhost:10011') as channel:
            stub = userStub(channel)
            response = await stub.listUser(Request())
            if response.code != 0:
                raise Exception("code not 0")
    asyncio.run(main())
