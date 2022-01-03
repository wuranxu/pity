import requests
from fastapi import APIRouter, Depends
from starlette import status

from app.crud.auth.UserDao import UserDao
from app.excpetions.RequestException import AuthException
from app.handler.fatcory import PityResponse
from app.middleware.Jwt import UserToken
from app.models.schema.user import UserUpdateForm
from app.routers import Permission, FORBIDDEN
from app.routers.auth.user_schema import UserDto, UserForm
from config import Config

router = APIRouter(prefix="/auth")


# router注册的函数都会自带/auth，所以url是/auth/register
@router.post("/register")
async def register(user: UserDto):
    try:
        await UserDao.register_user(**user.dict())
        return PityResponse.success(msg="注册成功, 请登录")
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/login")
async def login(data: UserForm):
    try:
        user = await UserDao.login(data.username, data.password)
        user = PityResponse.model_to_dict(user, "password")
        token = UserToken.get_token(user)
        return dict(code=0, msg="登录成功", data=dict(token=token, user=user))
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/listUser")
async def list_users(user_info=Depends(Permission())):
    try:
        users = UserDao.list_users()
        return PityResponse.success(PityResponse.model_to_list(users))
    except Exception as e:
        return PityResponse.failed(str(e))


@router.get("/github/login")
async def login_with_github(code: str):
    try:
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
            token = UserToken.get_token(user)
            return dict(code=0, msg="登录成功", data=dict(token=token, user=user))
    except:
        # 大部分原因是github出问题，忽略
        return dict(code=110, msg="登录超时, 请稍后再试")


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
        return PityResponse.success(PityResponse.model_to_dict(user))
    except AuthException as e:
        raise e
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/query")
async def update_user_info(token: str):
    try:
        if not token:
            raise AuthException(status.HTTP_200_OK, "token不存在")
        user_info = UserToken.parse_token(token)
        user = await UserDao.query_user(user_info['id'])
        return PityResponse.success(PityResponse.model_to_dict(user))
    except Exception as e:
        raise AuthException(status.HTTP_200_OK, e)


@router.get("/delete")
async def delete_user(id: int, user=Depends(Permission(Config.ADMIN))):
    # 此处要插入操作记录
    try:
        user = await UserDao.delete_user(id, user['id'])
        return PityResponse.success(PityResponse.model_to_dict(user))
    except Exception as e:
        return PityResponse.failed(e)
