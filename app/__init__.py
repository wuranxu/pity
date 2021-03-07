from flask import Flask

from app.controllers.auth.user import auth
from config import Config

pity = Flask(__name__)

# 注册蓝图
pity.register_blueprint(auth)

pity.config.from_object(Config)
