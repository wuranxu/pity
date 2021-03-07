from datetime import datetime

from app import pity
from app.utils.logger import Log
from app import dao


@pity.route('/')
def hello_world():
    log = Log("hello world")
    log.info("有人访问了你的网站了")
    now = datetime.now().strftime("%Y-%M-%d %H:%M:%S")
    print(now)
    return now


if __name__ == "__main__":
    pity.run("0.0.0.0", threaded=True, port="7777")
