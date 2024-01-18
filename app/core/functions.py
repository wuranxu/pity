import random
import uuid as uid
from datetime import datetime, timedelta

FMT = "%Y-%m-%d %H:%M:%S"
FMT_S = "%Y-%m-%d %H:%M:%S.%f+0000"


class PityFunction(object):

    @staticmethod
    def now(mode: int = 1):
        """
        获取当前时间 默认参数为1
        eg: now(2)
        :param mode: 模式
        1为当前时间戳，如 2023-09-15 11:00:00
        2为当前时间戳
        3为当前时间戳(毫秒级别)
        :return:
        """
        if mode == 1:
            return datetime.now().strftime(FMT)
        if mode == 2:
            return int(datetime.now().timestamp())
        if mode == 3:
            return int(datetime.now().timestamp()) * 1000

    @staticmethod
    def uuid():
        """
        获取当前uuid，常用于RequestId
        eg: uuid()
        :return:
        """
        return str(uid.uuid4()).replace("-", "")

    @staticmethod
    def sec_before(s: int):
        """
        获取N秒之前的时间戳
        eg: sec_before(30)
        :param s: 秒数
        :return:
        """
        return int(datetime.now().timestamp()) - s

    @staticmethod
    def hour_before(h: int):
        """
        获取N小时之前的时间戳
        eg: hour_before(6)
        :param h: 小时数
        :return:
        """
        return int(datetime.now().timestamp()) - 60 * 60 * h

    @staticmethod
    def day_before(d: int):
        """
        获取N天之前的时间戳
        eg: day_before(1)
        :param d: 天数
        :return:
        """
        return int(datetime.now().timestamp()) - 60 * 60 * 24 * d

    @staticmethod
    def get_unit(unit: str):
        if unit == "d":
            return "days"
        if unit == "h":
            return "hours"
        if unit == "s":
            return "seconds"

    @staticmethod
    def time_before(unit: str, num: int):
        """
        获取当前时间之前时间
        eg: time_before("d", 3)  获取3天前的时间戳
        :param unit: 单位，支持"d", "h", "s" 分别为天、小时、秒
        :param num: 数量
        :return:
        """
        ut = PityFunction.get_unit(unit)
        return datetime.now() - timedelta(**{ut: num})

    @staticmethod
    def time_after(unit: str, num: int):
        """
        获取当前时间之后时间
        eg: time_after("h", 3)
        :param unit: 单位，支持"d", "h", "s" 分别为天、小时、秒
        :param num: 数量
        :return:
        """
        ut = PityFunction.get_unit(unit)
        return datetime.now() + timedelta(**{ut: num})

    @staticmethod
    def random_int(a, b):
        """
        返回a~b之间的随机数
        eg: random_int(0, 30)
        :param a: 开始
        :param b: 结束
        :return:
        """
        return random.randint(a, b)
