from collections import namedtuple
from typing import Dict, List, Type, TypeVar

from fastapi import Header, APIRouter, Depends
from pydantic import BaseModel
from starlette import status

from app.crud import Mapper
from app.crud.auth.UserDao import UserDao
from app.exception.request import AuthException, PermissionException
from app.handler.fatcory import PityResponse
from app.middleware.Jwt import UserToken
from app.models import async_session
from config import Config

FORBIDDEN = "对不起, 你没有足够的权限"


class Permission:
    def __init__(self, role: int = Config.MEMBER):
        self.role = role

    async def __call__(self, token: str = Header(...)):
        if not token:
            raise AuthException(status.HTTP_200_OK, "用户信息身份认证失败, 请检查")
        try:
            user_info = UserToken.parse_token(token)
            if user_info.get("role", 0) < self.role:
                raise PermissionException(status.HTTP_200_OK, FORBIDDEN)
            user = await UserDao.query_user(user_info['id'])
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


_router: Dict[str, APIRouter] = {}
T = TypeVar("T", bound=BaseModel)
DAO = TypeVar("DAO", bound=Mapper)
CurdParams = namedtuple("parameters", ["name", "type_", "default", "like"])


class PityRouter(object):
    """
    pity路由基类，支持单标crud
    """

    def __init__(self, router: APIRouter, schema: Type[T], dao: Type[DAO], business, path, prefix="",
                 tags: List[str] = None, query_list: List[CurdParams] = None):
        self.router = router
        self.schema = schema
        self.dao = dao
        self.tags = tags
        self.business = business
        self.prefix = prefix
        self.path = path
        self.query_list = query_list

    @staticmethod
    def get_query_parameters(query: List[CurdParams]):
        params = ",".join(
            [f"{x.name}: {x.type_}" + (f" = '{x.default}'" if x.default is not None else "") for x in query])
        return params

    @staticmethod
    def get_query_sentence(query: List[CurdParams]):
        return ",".join([f"""{x.name}={x.name if not x.like else f"f'%{{{x.name}}}%'"}""" for x in query])

    def add_all(self):
        query = [] if self.query_list is None else self.query_list

        async def create(data: self.schema, user_info=Depends(AuthUser())):  # type: ignore
            model = data.dict()
            model.pop('id', None)
            result = await self.dao.insert(self.dao.model(**model, user=user_info.name))
            return PityResponse.success(result)

        params = ",".join([f"{x.name}: {x.type_}" for x in query])
        if params:
            params += ', '
        loc = dict(Permission=Permission, Depends=Depends, Response=PityResponse, self=self)
        list_func = f"""
    async def list_data({PityRouter.get_query_parameters(query)}):
        result = await self.dao.list_record({PityRouter.get_query_sentence(query)})
        return Response.ok(Response.model_to_list(result))
            """
        exec(list_func, loc)

        async def update(data: self.schema, user_info=Depends(AuthUser())):  # type: ignore
            result = await self.dao.update_by_id(data, user_info.name)
            return PityResponse.success(PityResponse.model_to_dict(result))

        async def delete(id: int, user_info=Depends(Permission())):
            await self.dao.delete_by_id(id)
            return PityResponse.success()

        self.router.add_api_route(f"{self.prefix}/{self.path}", create, tags=self.tags,
                                  summary=f"添加{self.business}", methods=['PUT'])

        self.router.add_api_route(f"{self.prefix}/{self.path}", update, tags=self.tags,
                                  summary=f"编辑{self.business}", methods=['POST'])

        self.router.add_api_route(f"{self.prefix}/{self.path}", delete, tags=self.tags,
                                  summary=f"删除{self.business}", methods=['DELETE'])

        self.router.add_api_route(f"{self.prefix}/{self.path}", loc.get("list_data"), tags=self.tags,
                                  summary=f"获取{self.business}", methods=['GET'])
