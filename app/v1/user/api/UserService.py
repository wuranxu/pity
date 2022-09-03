from app.crud.auth.UserDao import UserDao
from app.handler.fatcory import PityResponse
from app.middleware.Jwt import UserToken
from app.v1.dto.User import UserLoginRequest
from app.v1.user.proto.user_pb2_grpc import userServicer
from app.v1.utils.context import Context, ctx


class UserServiceApi(userServicer):

    @ctx
    async def login(self, request, context):
        data = Context.parse_args(request, UserLoginRequest)
        user = await UserDao.login(data.username, data.password)
        user = PityResponse.model_to_dict(user, "password")
        expire, token = UserToken.get_token(user)
        return Context.success(Context.dumps(dict(token=token, user=user, expire=expire), "password"))

    @ctx
    async def listUser(self, request, context):
        user = await UserDao.list_users()
        return Context.success(Context.dumps(user, "password"))

    @ctx
    async def register(self, request, context, ):
        data = Context.parse_args(request, UserLoginRequest)
        await UserDao.register_user(**data.dict())
        return Context.success()
