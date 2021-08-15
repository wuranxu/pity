from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

# 同步engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_recycle=1500)
# 异步engine
async_engine = create_async_engine(Config.ASYNC_SQLALCHEMY_URI, pool_recycle=1500)
Session = sessionmaker(engine)
async_session = sessionmaker(async_engine, class_=AsyncSession)
# 创建对象的基类:
Base = declarative_base()

Base.metadata.create_all(engine)


def update_model(dist, source, update_user=None, not_null=False):
    """
    :param dist:
    :param source:
    :param not_null:
    :param update_user:
    :return:
    """
    for var, value in vars(source).items():
        if not_null:
            if value:
                setattr(dist, var, value)
        else:
            setattr(dist, var, value)
        if update_user:
            setattr(dist, 'update_user', update_user)
        setattr(dist, 'updated_at', datetime.now())
