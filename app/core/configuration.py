import json
import os

from app.middleware.RedisManager import RedisHelper
from config import Config


class SystemConfiguration(object):
    """
    系统配置
    """

    @staticmethod
    @RedisHelper.cache("configuration", 24 * 3600)
    def get_config():
        try:
            filepath = os.path.join(Config.ROOT, "configuration.json")
            if not os.path.exists(filepath):
                raise Exception("没找到配置文件，请检查configuration文件是否已经被删除")
            with open(filepath, mode="r", encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"获取系统设置失败, {e}")

    @staticmethod
    @RedisHelper.up_cache("configuration")
    def update_config(config):
        try:
            filepath = os.path.join(Config.ROOT, "configuration.json")
            if not os.path.exists(filepath):
                raise Exception("没找到配置文件，请检查configuration文件是否已经被删除")
            with open(filepath, mode="r", encoding='utf-8') as f:
                json.dump(config, f)
        except Exception as e:
            raise Exception(f"更新系统设置失败, {e}")
