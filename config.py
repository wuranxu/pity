# 基础配置类
import os


class Config(object):
    ROOT = os.path.dirname(os.path.abspath(__file__))
    LOG_NAME = os.path.join(ROOT, 'logs', 'pity.log')
    # JSON_AS_ASCII = False  # Flask jsonify编码问题

    # MySQL连接信息
    MYSQL_HOST = "47.112.32.195"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "anrenear@33"
    # MYSQL_PWD = "wuranxu@33"
    DBNAME = "pity"

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
                                    MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, DBNAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 权限 0 普通用户 1 组长 2 管理员
    GUEST = 0
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

