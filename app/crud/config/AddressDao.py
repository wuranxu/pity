from app.crud import Mapper
from app.models.address import PityGateway
from app.utils.decorator import dao
from app.utils.logger import Log


@dao(PityGateway, Log("PityRedisConfigDao"))
class PityGatewayDao(Mapper):
    pass
