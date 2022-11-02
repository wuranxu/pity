import random
import time
from datetime import datetime

from sqlalchemy import or_, select, func
from sqlalchemy import update

from app.crud import Mapper
from app.middleware.Jwt import UserToken
from app.middleware.RedisManager import RedisHelper
from app.models import async_session
from app.models.user import User
from app.schema.user import UserUpdateForm
from app.utils.logger import Log
from config import Config


class UserDao(Mapper):
    log = Log("UserDao")

    @staticmethod
    @RedisHelper.up_cache("user_list")
    async def update_avatar(user_id: int, avatar_url: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = update(User).where(User.id == user_id).values(avatar=avatar_url)
                    await session.execute(sql)
        except Exception as e:
            UserDao.log.error(f"修改用户头像失败: {str(e)}")
            raise Exception(e)

    @staticmethod
    @RedisHelper.up_cache("user_list", "user_touch", key_and_suffix=("user_detail", lambda x: x[1]))
    async def update_user(user_info: UserUpdateForm, user_id: int):
        """
        变更用户的接口，主要用于用户管理页面(为管理员提供)
        :param user_id:
        :param user_info:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(select(User).where(User.id == user_info.id))
                    user = query.scalars().first()
                    if not user:
                        raise Exception("该用户不存在, 请检查")
                    # 开启not_null，这样只有非空字段才修改
                    UserDao.update_model(user, user_info, user_id, True)
                    await session.flush()
                    session.expunge(user)
                    return user
        except Exception as e:
            UserDao.log.error(f"修改用户信息失败: {str(e)}")
            raise Exception(e)

    @staticmethod
    @RedisHelper.up_cache("user_list", "user_touch", key_and_suffix=("user_detail", lambda x: x[0]))
    async def delete_user(id: int, user_id: int):
        """
        变更用户的接口，主要用于用户管理页面(为管理员提供)
        :param id: 被删除用户id
        :param user_id: 操作人id
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(select(User).where(User.id == id))
                    user = query.scalars().first()
                    if not user:
                        raise Exception("该用户不存在, 请检查")
                    if user.role == Config.ADMIN:
                        raise Exception("你不能删除超级管理员")
                    user.update_user = user_id
                    user.deleted_at = int(time.time() * 1000)
        except Exception as e:
            UserDao.log.error(f"修改用户信息失败: {str(e)}")
            raise Exception(e)

    @staticmethod
    @RedisHelper.up_cache("user_list", "user_touch")
    async def register_for_github(username, name, email, avatar):
        try:
            async with async_session() as session:
                async with session.begin():
                    # 异步session只需要 session.begin，下面的commit可以去掉 语法也有一些区别
                    query = await session.execute(
                        select(User).where(or_(User.username == username, User.email == email)))
                    user = query.scalars().first()
                    if user:
                        # 如果存在，则给用户更新信息
                        user.last_login_at = datetime.now()
                        user.name = name
                        user.avatar = avatar
                    else:
                        random_pwd = random.randint(100000, 999999)
                        user = User(username, name, UserToken.add_salt(str(random_pwd)), email, avatar)
                        session.add(user)
                    await session.flush()
                    session.expunge(user)
                    return user
        except Exception as e:
            UserDao.log.error(f"Github用户登录失败: {str(e)}")
            raise Exception("登录失败")

    @staticmethod
    @RedisHelper.up_cache("user_list", "user_touch")
    async def register_user(username: str, name: str, password: str, email: str):
        """
        :param username: 用户名
        :param name: 姓名
        :param password: 密码
        :param email: 邮箱
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    users = await session.execute(
                        select(User).where(or_(User.username == username, User.email == email)))
                    counts = await session.execute(select(func.count(User.id)))
                    if users.scalars().first():
                        raise Exception("用户名或邮箱已存在")
                    # 注册的时候给密码加盐
                    pwd = UserToken.add_salt(password)
                    user = User(username, name, pwd, email)
                    # 如果用户数量为0 则注册为超管
                    if counts.scalars().first() == 0:
                        user.role = Config.ADMIN
                    session.add(user)
        except Exception as e:
            UserDao.log.error(f"用户注册失败: {str(e)}")
            raise Exception(f"注册失败: {e}")

    @staticmethod
    async def login(username, password):
        """
        这里要改成异步了，原来的go写法要废弃
        :param username:
        :param password:
        :return:
        """
        try:
            pwd = UserToken.add_salt(password)
            async with async_session() as session:
                async with session.begin():
                    # 查询用户名/密码匹配且没有被删除的用户
                    query = await session.execute(
                        select(User).where(or_(User.username == username, User.email == username), User.password == pwd,
                                           User.deleted_at == 0))
                    user = query.scalars().first()
                    if user is None:
                        raise Exception("用户名或密码错误")
                    if not user.is_valid:
                        # 说明用户被禁用
                        raise Exception("您的账号已被封禁, 请联系管理员")
                    user.last_login_at = datetime.now()
                    await session.flush()
                    session.expunge(user)
                    return user
        except Exception as e:
            UserDao.log.error(f"用户{username}登录失败: {str(e)}")
            raise e

    @staticmethod
    @RedisHelper.cache("user_list", 3 * 3600)
    async def list_users():
        try:
            async with async_session() as session:
                query = await session.execute(select(User))
                return query.scalars().all()
        except Exception as e:
            UserDao.log.error(f"获取用户列表失败: {str(e)}")
            raise Exception("获取用户列表失败")

    @staticmethod
    @RedisHelper.cache("user_detail", 3600)
    async def query_user(id: int):
        async with async_session() as session:
            query = await session.execute(select(User).where(User.id == id))
            return query.scalars().first()

    @staticmethod
    @RedisHelper.cache("user_touch")
    async def list_user_touch(*user):
        try:
            if not user:
                return []
            async with async_session() as session:
                query = await session.execute(select(User).where(User.id.in_(user), User.deleted_at == 0))
                return [{"email": q.email, "phone": q.phone} for q in query.scalars().all()]
        except Exception as e:
            UserDao.log.error(f"获取用户联系方式失败: {str(e)}")
            raise Exception(f"获取用户联系方式失败: {e}")

    @staticmethod
    async def reset_password(email: str, password: str):
        pwd = UserToken.add_salt(password)
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = update(User).where(User.email == email).values(password=pwd)
                    await session.execute(sql)
        except Exception as e:
            UserDao.log.error(f"重置用户: {email}密码失败: {str(e)}")
            raise Exception(f"重置{email}密码失败")

    @staticmethod
    async def query_user_by_email(email: str):
        async with async_session() as session:
            sql = select(User).where(User.email == email, User.is_valid == True)
            query = await session.execute(sql)
            return query.scalars().first()
