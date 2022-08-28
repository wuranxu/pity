import json

from app.crud.auth.UserDao import UserDao
from app.handler.encoder import JsonEncoder
from app.handler.fatcory import PityResponse
from app.middleware.Jwt import UserToken
from app.v1.user.proto.user_pb2 import Response
from app.v1.user.proto.user_pb2_grpc import userServicer


class UserServiceApi(userServicer):

    async def login(self, request, context):
        data = json.loads(request.requestJson.decode("utf-8"))
        user = await UserDao.login(data.get("username"), data.get("password"))
        user = PityResponse.model_to_dict(user, "password")
        expire, token = UserToken.get_token(user)
        res = json.dumps(dict(token=token, user=user, expire=expire), cls=JsonEncoder, ensure_ascii=False)
        resp = Response(resultJson=res.encode("utf-8"), code=0, msg="登录成功")
        return resp
