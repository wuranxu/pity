import random
from datetime import datetime

from sqlalchemy import or_, select

from app.middleware.Jwt import UserToken
from app.models import Session, async_session
from app.models.user import User
from app.utils.logger import Log


class UserDao(object):
    log = Log("UserDao")

    @staticmethod
    def register_for_github(username, name, email, avatar):
        try:
            with Session() as session:
                user = session.query(User).filter(or_(User.username == username, User.email == email)).first()
                if user:
                    # 如果存在，则给用户更新信息
                    user.last_login_at = datetime.now()
                    user.name = name
                    user.avatar = avatar
                else:
                    random_pwd = random.randint(100000, 999999)
                    user = User(username, name, UserToken.add_salt(str(random_pwd)), email, avatar)
                    session.add(user)
                session.commit()
                session.refresh(user)
                return user
        except Exception as e:
            UserDao.log.error(f"Github用户登录失败: {str(e)}")
            raise Exception("登录失败")

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
            with Session() as session:
                users = session.query(User).filter(or_(User.username == username, User.email == email)).all()
                if users:
                    raise Exception("用户名或邮箱已存在")
                # 注册的时候给密码加盐
                pwd = UserToken.add_salt(password)
                user = User(username, name, pwd, email)
                session.add(user)
                session.commit()
        except Exception as e:
            UserDao.log.error(f"用户注册失败: {str(e)}")
            return str(e)
        return None

    @staticmethod
    def login(username, password):
        try:
            pwd = UserToken.add_salt(password)
            with Session() as session:
                # 查询用户名/密码匹配且没有被删除的用户
                user = session.query(User).filter_by(username=username, password=pwd, deleted_at=None).first()
                if user is None:
                    return None, "用户名或密码错误"
                # 更新用户的最后登录时间
                user.last_login_at = datetime.now()
                session.commit()
                session.refresh(user)
                return user, None
        except Exception as e:
            UserDao.log.error(f"用户{username}登录失败: {str(e)}")
            return None, str(e)

    @staticmethod
    def list_users():
        try:
            with Session() as session:
                users = session.query(User).filter_by(deleted_at=None).all()
                return users, None
        except Exception as e:
            UserDao.log.error(f"获取用户列表失败: {str(e)}")
            return [], str(e)

    @staticmethod
    async def list_user_email(*user):
        try:
            if not user:
                return []
            async with async_session() as session:
                query = await session.execute(select(User).where(User.id.in_(user), User.deleted_at == None))
                return [q.email for q in query.scalars().all()]
        except Exception as e:
            UserDao.log.error(f"获取用户邮箱失败: {str(e)}")
            raise Exception(f"获取用户邮箱失败: {e}")
