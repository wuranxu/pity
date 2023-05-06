import asyncio

import requests
from fastapi import APIRouter, Depends
from starlette import status

from app.core.msg.mail import Email
from app.crud.auth.UserDao import UserDao
from app.exception.request import AuthException
from app.handler.fatcory import PityResponse
from app.middleware.Jwt import UserToken
from app.routers import Permission, FORBIDDEN
from app.schema.user import UserUpdateForm, UserForm, UserDto, ResetPwdForm
from app.utils.des import Des
from config import Config

router = APIRouter(prefix="/auth")


# router注册的函数都会自带/auth，所以url是/auth/register
@router.post("/register")
async def register(user: UserDto):
    try:
        user = await UserDao.register_user(**user.dict())
        user = PityResponse.model_to_dict(user, "password")
        expire, token = UserToken.get_token(user)
        return PityResponse.success(dict(token=token, user=user, expire=expire), msg="注册成功, 请登录")
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/login")
async def login(data: UserForm):
    try:
        user = await UserDao.login(data.username, data.password)
        user = PityResponse.model_to_dict(user, "password")
        expire, token = UserToken.get_token(user)
        return PityResponse.success(dict(token=token, user=user, expire=expire), msg="登录成功")
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/listUser")
async def list_users(_=Depends(Permission())):
    try:
        user = await UserDao.list_users()
        return PityResponse.success(user, exclude=("password",))
    except Exception as e:
        return PityResponse.failed(str(e))


@router.get("/github/login")
async def login_with_github(code: str):
    try:
        code = code.rstrip("#/")
        with requests.Session() as session:
            r = session.get(Config.GITHUB_ACCESS, params=dict(client_id=Config.CLIENT_ID,
                                                              client_secret=Config.SECRET_KEY,
                                                              code=code), timeout=8)
            token = r.text.split("&")[0].split("=")[1]
            res = session.get(Config.GITHUB_USER, headers={"Authorization": "token {}".format(token)}, timeout=8)
            user_info = res.json()
            user = await UserDao.register_for_github(user_info.get("login"), user_info.get("name"),
                                                     user_info.get("email"),
                                                     user_info.get("avatar_url"))
            user = PityResponse.model_to_dict(user, "password")
            expire, token = UserToken.get_token(user)
            return PityResponse.success(dict(token=token, user=user, expire=expire), msg="登录成功")
    except:
        # 大部分原因是github出问题，忽略
        return PityResponse.failed(code=110, msg="登录超时, 请稍后再试")


@router.post("/update")
async def update_user_info(user_info: UserUpdateForm, user=Depends(Permission(Config.MEMBER))):
    try:
        if user['role'] != Config.ADMIN:
            if user['id'] != user_info.id:
                # 既不是改自己的资料，也不是超管
                return PityResponse.failed(FORBIDDEN)
            # 如果不是超管，说明是自己改自己，不允许自己改自己的角色
            user_info.role = None
        user = await UserDao.update_user(user_info, user['id'])
        return PityResponse.success(user, exclude=("password", "phone", "email"))
    except AuthException as e:
        raise e
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/query")
async def query_user_info(token: str):
    try:
        if not token:
            raise AuthException(status.HTTP_200_OK, "token不存在")
        user_info = UserToken.parse_token(token)
        user = await UserDao.query_user(user_info['id'])
        if user is None:
            return PityResponse.failed("用户不存在")
        return PityResponse.success(user, exclude=("password",))
    except Exception as e:
        # raise AuthException(status.HTTP_200_OK, e)
        return PityResponse.failed(e)


@router.get("/delete")
async def delete_user(id: int, user=Depends(Permission(Config.ADMIN))):
    # 此处要插入操作记录
    try:
        user = await UserDao.delete_user(id, user['id'])
        return PityResponse.success(user)
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/reset", summary="重置用户密码")
async def reset_user(form: ResetPwdForm):
    email = Des.des_decrypt(form.token)
    await UserDao.reset_password(email, form.password)
    return PityResponse.success()


@router.get("/reset/generate/{email}", summary="生成重置密码链接")
async def generate_reset_url(email: str):
    try:
        user = await UserDao.query_user_by_email(email)
        if user is not None:
            # 说明邮件存在，发送邮件
            em = Des.des_encrypt(email)
            link = f"""https://pity.fun/#/user/resetPassword?token={em}"""
            render_html = Email.render_html(Config.PASSWORD_HTML_PATH, link=link, name=user.name)
            asyncio.create_task(Email.send_msg("重置你的pity密码", render_html, None, email))
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(str(e))


@router.get("/reset/check/{token}", summary="检测生成的链接是否正确")
async def check_reset_url(token: str):
    try:
        email = Des.des_decrypt(token)
        return PityResponse.success(email)
    except:
        return PityResponse.failed("重置链接不存在, 请不要无脑尝试")
