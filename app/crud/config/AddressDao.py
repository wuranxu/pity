from sqlalchemy import select

from app.crud import Mapper
from app.models import async_session
from app.models.address import PityGateway
from app.utils.logger import Log


class PityGatewayDao(Mapper, metaclass=Mapper):
    __log__ = Log("PityRedisConfigDao")
    __model__ = PityGateway

    @staticmethod
    # @RedisHelper.cache(f"gateway", 1800)
    async def query_gateway(env, name):
        async with async_session() as session:
            query = await session.execute(select(PityGateway).where(PityGateway.deleted_at == 0, PityGateway.env == env,
                                                                    PityGateway.name == name))
            data = query.scalars().first()
            if data is None:
                raise Exception(f"此环境没有网关配置: {name}")
            return data.gateway
