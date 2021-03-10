from datetime import datetime

from app import pity
from app.controllers.request.http import req
from app.utils.logger import Log
from app.controllers.auth.user import auth

# 注册蓝图
pity.register_blueprint(auth)
pity.register_blueprint(req)


@pity.route('/')
def hello_world():
    log = Log("hello world")
    log.info("有人访问了你的网站了")
    now = datetime.now().strftime("%Y-%M-%d %H:%M:%S")
    print(now)
    return now


if __name__ == "__main__":
    pity.run("0.0.0.0", threaded=True, port="7777")
