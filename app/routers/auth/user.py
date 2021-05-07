from fastapi import APIRouter, Depends

from app.dao.auth.UserDao import UserDao
from app.handler.fatcory import ResponseFactory
from app.middleware.Jwt import UserToken
from app.routers import Permission
from app.routers.auth.user_schema import UserDto, UserForm

router = APIRouter(prefix="/auth")


# router注册的函数都会自带/auth，所以url是/auth/register
@router.post("/register")
async def register(user: UserDto):
    err = UserDao.register_user(**user.dict())
    if err is not None:
        return dict(code=110, msg=err)
    return dict(code=0, msg="注册成功")


@router.post("/login")
async def login(data: UserForm):
    user, err = UserDao.login(data.username, data.password)
    if err is not None:
        return dict(code=110, msg=err)
    user = ResponseFactory.model_to_dict(user, "password")
    token = UserToken.get_token(user)
    if err is not None:
        return dict(code=110, msg=err)
    return dict(code=0, msg="登录成功", data=dict(token=token, user=user))


@router.get("/listUser")
async def list_users(user_info=Depends(Permission())):
    users, err = UserDao.list_users()
    if err is not None:
        return dict(code=110, msg=err)
    return dict(code=0, msg="操作成功", data=ResponseFactory.model_to_list(users))
