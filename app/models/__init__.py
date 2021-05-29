# from flask_sqlalchemy import SQLAlchemy
#
# from app import pity
#
# db = SQLAlchemy(pity)
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_recycle=1500)
Session = sessionmaker(engine)
# 创建对象的基类:
Base = declarative_base()

# from app.models import engine, Base

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
