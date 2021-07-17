from datetime import datetime
from functools import wraps


class SingletonDecorator:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


def case_log(func):
    @wraps(func)
    def wrapper(*args, **kw):
        cls = args[0]
        doc = func.__doc__
        cls.logger.append("[{}]: 步骤开始 -> {} 参数: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                           doc.strip() if doc else func.__name__, get_str(args, kw)))
        returns = func(*args, **kw)
        cls.logger.append("[{}]: 步骤结束 -> {} {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                       doc.strip() if doc else func.__name__, get_returns(returns)))
        return returns

    return wrapper


def get_str(args, kwargs):
    result = []
    # 这里从1索引开始，是因为args[0]是self, 也就注定了case_log只能在Executor方法下使用
    for a in args[1:]:
        if type(a).__name__ == "function":
            result.append(a.__doc__ if a.__doc__ else a.__name__)
        else:
            result.append(str(a))
    if kwargs:
        for k, v in kwargs:
            result.append(f"{k}->{v}")
    if len(result) == 0:
        return "无"
    return ", ".join(result)


def get_returns(obj):
    if not obj:
        return ""
    if type(obj).__name__ == "function":
        return obj.__doc__ if obj.__doc__ else obj.__name__
    if isinstance(obj, object):
        return str(obj)
    return f"返回值: {obj}"
