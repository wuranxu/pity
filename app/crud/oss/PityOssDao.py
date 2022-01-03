from app.crud import Mapper
from app.models.oss_file import PityOssFile
from app.utils.decorator import dao
from app.utils.logger import Log


@dao(PityOssFile, Log("PityOssDao"))
class PityOssDao(Mapper):
    pass
