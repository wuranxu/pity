# 基础配置类
import os


class Config(object):
    ROOT = os.path.dirname(os.path.abspath(__file__))
    LOG_NAME = os.path.join(ROOT, 'logs', 'pity.log')
    # JSON_AS_ASCII = False  # Flask jsonify编码问题

    # MySQL连接信息
    MYSQL_HOST = "121.5.2.74"
    # MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    # MYSQL_PWD = "anrenear@33"
    MYSQL_PWD = "wuranxu@33"
    DBNAME = "pity"

    REDIS_HOST = "121.5.2.74"
    REDIS_PORT = 7788
    REDIS_DB = 0
    REDIS_PASSWORD = "woodywu"

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
    # CLIENT_ID = "c46c7ae33442d13498cd"

    # SECRET
    SECRET_KEY = "a13c22377318291d5932bc5b62c1885b344355a0"

    # SECRET_KEY = "c79fafe58ff45f6b5b51ddde70d2d645209e38b9"

    # 测试报告路径
    REPORT_PATH = os.path.join(ROOT, "templates", "report.html")

    SERVER_REPORT = "http://test.pity.fun/#/record/report/"

    # 请求类型
    class BodyType:
        none = 0
        json = 1
        form = 2
        x_form = 3
        binary = 4
        graphQL = 5
