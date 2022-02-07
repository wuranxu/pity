# 基础配置类
import os
from enum import IntEnum


class BaseConfig(object):
    ROOT = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(ROOT, 'logs')
    LOG_NAME = os.path.join(LOG_DIR, 'pity.log')
    # JSON_AS_ASCII = False  # Flask jsonify编码问题

    # MySQL连接信息
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "wuranxu@33"
    DBNAME = "pity"

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 7788
    REDIS_DB = 0
    REDIS_PASSWORD = "woodywu123"

    # Redis连接信息
    REDIS_NODES = [{"host": REDIS_HOST, "port": REDIS_PORT, "db": REDIS_DB, "password": REDIS_PASSWORD}]

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
        MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, DBNAME)

    # 异步URI
    ASYNC_SQLALCHEMY_URI = f'mysql+aiomysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{DBNAME}'
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
    CLIENT_ID = "0f4fc0a875de30614a6a"

    # SECRET
    SECRET_KEY = "a13c22377318291d5932bc5b62c1885b344355a0"

    # 测试报告路径
    REPORT_PATH = os.path.join(ROOT, "templates", "report.html")

    # APP 路径
    APP_PATH = os.path.join(ROOT, "app")

    # dao路径
    DAO_PATH = os.path.join(APP_PATH, 'crud')

    SERVER_REPORT = "http://localhost:8000/#/record/report/"

    ALIYUN = "aliyun"
    GITEE = "gitee"

    RELATION = "pity_relation"
    ALIAS = "__alias__"
    TABLE_TAG = "__tag__"
    # 数据库表展示的变更字段
    FIELD = "__fields__"
    SHOW_FIELD = "__show__"
    IGNORE_FIELDS = ('created_at', "updated_at", "deleted_at", "create_user", "update_user")

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

    # 日志名
    PITY_ERROR = "pity_error"
    PITY_INFO = "pity_info"


class DevConfig(BaseConfig):
    pass


class ProConfig(BaseConfig):
    MYSQL_HOST = "121.5.2.74"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "wuranxu@33"
    DBNAME = "pity"

    REDIS_HOST = "121.5.2.74"
    REDIS_PORT = 7788
    REDIS_DB = 0
    REDIS_PASSWORD = "woodywu123"

    # Redis连接信息
    REDIS_NODES = [{"host": REDIS_HOST, "port": REDIS_PORT, "db": REDIS_DB, "password": REDIS_PASSWORD}]

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
        MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, DBNAME)

    # 异步URI
    ASYNC_SQLALCHEMY_URI = f'mysql+aiomysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{DBNAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CLIENT_ID = "c46c7ae33442d13498cd"
    SECRET_KEY = "c79fafe58ff45f6b5b51ddde70d2d645209e38b9"

    SERVER_REPORT = "http://121.5.2.74/#/record/report/"


# 获取pity环境变量
PITY_ENV = os.environ.get("pity_env", "dev")
# 如果pity_env存在且为prod
Config = ProConfig() if PITY_ENV and PITY_ENV.lower() == "pro" else DevConfig()
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
