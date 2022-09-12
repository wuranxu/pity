import time

import grpc
from locust import task, User
from locust.exception import LocustError

from request_pb2 import Request
from user.proto.user_pb2_grpc import userStub


class GrpcClient:
    def __init__(self, environment, stub):
        self.env = environment
        self._stub_class = stub.__class__
        self._stub = stub

    def __getattr__(self, name):
        func = self._stub_class.__getattribute__(self._stub, name)

        def wrapper(*args, **kwargs):
            request_meta = {
                "request_type": "grpc",
                "name": name,
                "start_time": time.time(),
                "response_length": 0,
                "exception": None,
                "context": None,
                "response": None,
            }
            start_perf_counter = time.perf_counter()
            try:
                resp = func(*args, **kwargs)
                request_meta["response"] = resp
                request_meta["response_length"] = len(resp.resultJson)
                if resp.code == 0:
                    raise grpc.RpcError("状态码为0了")
                print(resp)
            except grpc.RpcError as e:
                request_meta["exception"] = e
            request_meta["response_time"] = (time.perf_counter() - start_perf_counter) * 1000
            self.env.events.request.fire(**request_meta)
            return request_meta["response"]

        return wrapper


class GrpcUser(User):
    abstract = True

    stub_class = None

    def __init__(self, environment):
        super().__init__(environment)
        for attr_value, attr_name in ((self.host, "host"), (self.stub_class, "stub_class")):
            if attr_value is None:
                raise LocustError(f"You must specify the {attr_name}.")
        self._channel = grpc.insecure_channel(self.host)
        self._channel_closed = False
        stub = self.stub_class(self._channel)
        self.client = GrpcClient(environment, stub)


class HelloGrpcUser(GrpcUser):
    host = "localhost:50051"
    stub_class = userStub

    @task
    def sayHello(self):
        string = """
                {
            "username": "woody",
            "password": "wujranxu"
        }
                """
        if not self._channel_closed:
            self.client.login(Request(requestJson=string.encode("utf-8")))
