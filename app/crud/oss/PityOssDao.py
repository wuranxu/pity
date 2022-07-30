from app.crud import Mapper, ModelWrapper
from app.models.oss_file import PityOssFile


@ModelWrapper(PityOssFile)
class PityOssDao(Mapper):
    pass
