from datetime import datetime

from sqlalchemy import or_

from app.middleware.Jwt import UserToken
from app.models import db
from app.models.user import User
from app.utils.logger import Log


class UserDao(object):
    log = Log("UserDao")

    @staticmethod
    def register_user(username, name, password, email):
        """

        :param username: 用户名
        :param name: 姓名
        :param password: 密码
        :param email: 邮箱
        :return:
        """
        try:
            users = User.query.filter(or_(User.username == username, User.email == email)).all()
            if users:
                raise Exception("用户名或邮箱已存在")
            # 注册的时候给密码加盐
            pwd = UserToken.add_salt(password)
            user = User(username, name, pwd, email)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            UserDao.log.error(f"用户注册失败: {str(e)}")
            return str(e)
        return None

    @staticmethod
    def login(username, password):
        try:
            pwd = UserToken.add_salt(password)
            # 查询用户名/密码匹配且没有被删除的用户
            user = User.query.filter_by(username=username, password=pwd, deleted_at=None).first()
            if user is None:
                return None, "用户名或密码错误"
            # 更新用户的最后登录时间
            user.last_login_at = datetime.now()
            db.session.commit()
            return user, None
        except Exception as e:
            UserDao.log.error(f"用户{username}登录失败: {str(e)}")
            return None, str(e)

    @staticmethod
    def list_users():
        try:
            users = User.query.filter_by(deleted_at=None).all()
            return users, None
        except Exception as e:
            UserDao.log.error(f"获取用户列表失败: {str(e)}")
            return [], str(e)
