# 基础配置类
import os
from enum import IntEnum
from typing import List

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    ROOT = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(ROOT, 'logs')
    LOG_NAME = os.path.join(LOG_DIR, 'pity.log')

    SERVER_PORT: int

    # mock server
    MOCK_ON: bool
    MOCK_PORT: int
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PWD: str
    DBNAME: str

    # WARNING: close redis can make job run multiple times at the same time
    REDIS_ON: bool
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str
    # Redis连接信息
    REDIS_NODES: List[dict] = []

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI: str = ''
    # 异步URI
    ASYNC_SQLALCHEMY_URI: str = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 权限 0 普通用户 1 组长 2 管理员
    MEMBER = 0
    MANAGER = 1
    ADMIN = 2

    # github access_token地址
    GITHUB_ACCESS = "https://github.com/login/oauth/access_token"

    # github获取用户信息
    GITHUB_USER = "https://api.github.com/user"

    # client_id
    CLIENT_ID: str

    # SECRET
    SECRET_KEY: str

    # 测试报告路径
    REPORT_PATH = os.path.join(ROOT, "templates", "report.html")

    # APP 路径
    APP_PATH = os.path.join(ROOT, "app")

    # dao路径
    DAO_PATH = os.path.join(APP_PATH, 'crud')

    # markdown地址
    MARKDOWN_PATH = os.path.join(ROOT, 'templates', "markdown")

    SERVER_REPORT = "http://localhost:8000/#/record/report/"

    OSS_URL = "http://oss.pity.fun"

    # 七牛云链接地址，如果采用七牛oss，需要自行替换
    QINIU_URL = "https://static.pity.fun"

    RELATION = "pity_relation"
    ALIAS = "__alias__"
    TABLE_TAG = "__tag__"
    # 数据库表展示的变更字段
    FIELD = "__fields__"
    SHOW_FIELD = "__show__"
    IGNORE_FIELDS = ('created_at', "updated_at", "deleted_at", "create_user", "update_user")

    # 测试计划中，case默认重试次数
    RETRY_TIMES = 1

    # 请求类型
    class BodyType(IntEnum):
        none = 0
        json = 1
        form = 2
        x_form = 3
        binary = 4
        graphQL = 5

    # 全局变量的类型
    class GconfigType:
        case = 0
        constructor = 1
        asserts = 2

        @staticmethod
        def value(val):
            if val == 0:
                return "用例"
            if val == 1:
                return "前后置条件"
            return "断言"

    # 前置条件类型
    class ConstructorType:
        testcase = 0
        sql = 1
        redis = 2
        py_script = 3
        http = 4

    # 日志类型
    class OperationType:
        INSERT = 0
        UPDATE = 1
        DELETE = 2
        EXECUTE = 3
        STOP = 4

    # 通知类型
    class NoticeType(IntEnum):
        EMAIL = 0
        DINGDING = 1
        WECHAT = 2
        FEISHU = 3

    # 日志名
    PITY_ERROR = "pity_error"
    PITY_INFO = "pity_info"


class DevConfig(BaseConfig):
    class Config:
        env_file = "./conf/dev.env"


class ProConfig(BaseConfig):
    class Config:
        env_file = "./conf/pro.env"

    SERVER_REPORT = "https://pity.fun/#/record/report/"


# 获取pity环境变量
PITY_ENV = os.environ.get("pity_env", "dev")
# 如果pity_env存在且为prod
Config = ProConfig() if PITY_ENV and PITY_ENV.lower() == "pro" else DevConfig()

# init redis
Config.REDIS_NODES = [
    {
        "host": Config.REDIS_HOST, "port": Config.REDIS_PORT, "db": Config.REDIS_DB, "password": Config.REDIS_PASSWORD
    }
]

# init sqlalchemy (used by apscheduler)
Config.SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
    Config.MYSQL_USER, Config.MYSQL_PWD, Config.MYSQL_HOST, Config.MYSQL_PORT, Config.DBNAME)

# init async sqlalchemy
Config.ASYNC_SQLALCHEMY_URI = f'mysql+aiomysql://{Config.MYSQL_USER}:{Config.MYSQL_PWD}' \
                              f'@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.DBNAME}'

BANNER = """
 ________        ___          _________         ___    ___ 
|\   __  \      |\  \        |\___   ___\      |\  \  /  /|
\ \  \|\  \     \ \  \       \|___ \  \_|      \ \  \/  / /
 \ \   ____\     \ \  \           \ \  \        \ \    / / 
  \ \  \___|      \ \  \           \ \  \        \/  /  /  
   \ \__\          \ \__\           \ \__\     __/  / /    
    \|__|           \|__|            \|__|    |\___/ /     
                                              \|___|/      

"""
