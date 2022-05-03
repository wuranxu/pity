from app.core.configuration import SystemConfiguration
from app.enums.OssEnum import OssEnum
from app.middleware.oss.aliyun import AliyunOss
from app.middleware.oss.files import OssFile
from app.middleware.oss.qiniu import QiniuOss
from app.middleware.oss.tencent import TencentCos


class OssClient(object):
    _client = None

    @classmethod
    def get_oss_client(cls) -> OssFile:
        """
        通过oss配置拿到oss客户端
        :return:
        """
        if OssClient._client is None:
            cfg = SystemConfiguration.get_config()
            oss_config = cfg.get("oss")
            access_key_id = oss_config.get("access_key_id")
            access_key_secret = oss_config.get("access_key_secret")
            bucket = oss_config.get("bucket")
            endpoint = oss_config.get("endpoint")
            if oss_config is None:
                raise Exception("服务器未配置oss信息, 请在configuration.json中添加")
            if oss_config.get("oss_type").lower() == OssEnum.ALIYUN.value:
                return AliyunOss(access_key_id, access_key_secret, endpoint, bucket)
            if oss_config.get("oss_type").lower() == OssEnum.QINIU.value:
                return QiniuOss(access_key_id, access_key_secret, bucket)
            if oss_config.get("oss_type").lower() == OssEnum.TENCENT.value:
                return TencentCos(access_key_id, access_key_secret, endpoint, bucket)
            raise Exception("不支持的oss类型")
        return OssClient._client
