from fastapi import Header
from starlette import status

from app.excpetions.RequestException import AuthException, PermissionException
from app.middleware.Jwt import UserToken
from app.models import async_session
from config import Config

FORBIDDEN = "对不起, 你没有足够的权限"


class Permission:
    def __init__(self, role: int = Config.MEMBER):
        self.role = role

    def __call__(self, token: str = Header(...)):
        if not token:
            raise AuthException(status.HTTP_200_OK, "用户信息身份认证失败, 请检查")
        try:
            user_info = UserToken.parse_token(token)
            if user_info.get("role", 0) < self.role:
                raise PermissionException(status.HTTP_200_OK, FORBIDDEN)
        except PermissionException as e:
            raise e
        except Exception as e:
            raise AuthException(status.HTTP_200_OK, str(e))
        return user_info


async def get_session():
    """
    获取异步session
    :return:
    """
    async with async_session() as session:
        yield session
