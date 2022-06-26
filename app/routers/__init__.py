import asyncio

from fastapi import Header
from starlette import status

from app.crud.auth.UserDao import UserDao
from app.excpetions.RequestException import AuthException, PermissionException
from app.handler.fatcory import PityResponse
from app.middleware.Jwt import UserToken
from app.models import async_session
from app.utils.internal import synchronize_async_helper
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
            user = synchronize_async_helper(UserDao.query_user(user_info['id']))
            if user is None:
                raise Exception("用户不存在")
            user_info = PityResponse.model_to_dict(user, "password")
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

# _router: Dict[str, APIRouter] = {}
#
#
# class PityRouter(object):
#     """
#     pity路由基类，支持单标crud
#     """
#
#     def __init__(self, group: str, schema: PityModel = None, path: str = "", read: int = Config.MEMBER,
#                  write: int = Config.MANAGER, operation_log: bool = True):
#         """
#         初始化路由相关数据，包括schema，path，权限等
#         :param group:
#         :param schema:
#         :param path:
#         :param read:
#         :param write:
#         :param operation_log:
#         """
#         self.group = group
#         self.schema = schema
#         self.path = path
#         self.read = read
#         self.write = write
#         self.operation_log = operation_log
#
#     def _get_router(self):
#         router = _router.get(self.group)
#         if router is None:
#             router = APIRouter(prefix=self.group)
#             _router[self.group] = router
#         return router
#
#     def generate_router(self):
#         router = self._get_router()
#         router.add_api_route(f"{self.path}/list", self._list(), methods=['GET'], response_model=None)
#         return router
#
#     def _list(self):
#         schema = self.schema
#
#         def route(query: Query):
#             print(query)
#             return PityResponse.success()
#
#         return route
#
#     def _query(self):
#         pass
#
#     def _update(self):
#         pass
