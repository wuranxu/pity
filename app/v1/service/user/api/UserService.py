import asyncio

from app.core.msg.mail import Email
from app.crud.auth.UserDao import UserDao
from app.excpetions.AuthException import AuthException
from app.handler.fatcory import PityResponse
from app.middleware.Jwt import UserToken
from app.routers import FORBIDDEN
from app.schema.user import UserUpdateForm, ResetPwdForm
from app.utils.des import Des
from app.v1.dto.User import UserLoginRequest, UserQueryRequest, GenerateUrlRequest, UserRegisterRequest
from app.v1.service.user.proto.user_pb2_grpc import userServicer
from app.v1.utils.context import Context, ctx
from config import Config


class UserServiceApi(userServicer):

    @ctx
    async def login(self, request, context):
        """
        用户登录
        :param request:
        :param context:
        :return:
        """
        data = Context.parse_args(request, UserLoginRequest)
        user = await UserDao.login(data.username, data.password)
        user = PityResponse.model_to_dict(user, "password")
        expire, token = UserToken.get_token(user)
        return Context.success(Context.dumps(dict(token=token, user=user, expire=expire), "password"))

    @ctx
    async def listUser(self, request, context):
        """
        获取用户列表
        :param request:
        :param context:
        :return:
        """
        user = await UserDao.list_users()
        return Context.success(Context.dumps(user, "password"))

    @ctx
    async def register(self, request, context):
        """
        注册用户
        :param request:
        :param context:
        :return:
        """
        data = Context.parse_args(request, UserRegisterRequest)
        await UserDao.register_user(**data.dict())
        return Context.success()

    @ctx
    async def update(self, request, context):
        """
        更新用户信息
        :param request:
        :param context:
        :return:
        """
        user = Context.parse_args(request, UserUpdateForm)
        user_info = Context.get_user(context)
        if user.role != Config.ADMIN:
            if user_info.id != user.id:
                # 既不是改自己的资料，也不是超管
                return Context.failed(FORBIDDEN)
            # 如果不是超管，说明是自己改自己，不允许自己改自己的角色
            user_info.role = None
        user = await UserDao.update_user(user, user_info.id)
        return Context.success(Context.dumps(user, *("password", "phone", "email")))

    @ctx
    async def query(self, request, context):
        """
        查询当前用户信息
        :param request:
        :param context:
        :return:
        """
        token = Context.parse_args(request, UserQueryRequest)
        if not token:
            raise AuthException("token不存在")
        user_info = UserToken.parse_token(token)
        user = await UserDao.query_user(user_info['id'])
        if user is None:
            return Context.failed("用户不存在")
        return Context.success(Context.dumps(user, "password"))

    @ctx
    async def delete(self, request, context):
        """
        删除用户
        :param request:
        :param context:
        :return:
        """
        user = Context.parse_args(request, UserQueryRequest)
        user_info = Context.get_user(context)
        user = await UserDao.delete_user(user.id, user_info.id)
        return Context.success(user)

    @ctx
    async def resetPassword(self, request, context):
        """
        重置用户密码
        :param request:
        :param context:
        :return:
        """
        form = Context.parse_args(request, ResetPwdForm)
        email = Des.des_decrypt(form.token)
        await UserDao.reset_password(email, form.password)
        return Context.success()

    @ctx
    async def checkToken(self, request, context):
        """

        :param request:
        :param context:
        :return:
        """
        form = Context.parse_args(request, ResetPwdForm)
        email = Des.des_decrypt(form.token)
        await UserDao.reset_password(email, form.password)

    @ctx
    async def generatePassword(self, request, context):
        """
        生成密码
        :param request:
        :param context:
        :return:
        """
        form = Context.parse_args(request, GenerateUrlRequest)
        user = await UserDao.query_user_by_email(form.email)
        if user is not None:
            # 说明邮件存在，发送邮件
            em = Des.des_encrypt(form.email)
            link = f"""https://pity.fun/#/user/resetPassword?token={em}"""
            render_html = Email.render_html(Config.PASSWORD_HTML_PATH, link=link, name=user.name)
            asyncio.create_task(Email.send_msg("重置你的pity密码", render_html, None, form.email))
        return Context.success()
