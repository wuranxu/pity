# from flask_sqlalchemy import SQLAlchemy
#
# from app import pity
#
# db = SQLAlchemy(pity)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(engine)
# 创建对象的基类:
Base = declarative_base()

# from app.models import engine, Base

Base.metadata.create_all(engine)

