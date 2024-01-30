"""
通过jinja2模板引擎解析上下文
"""
from functools import lru_cache

from jinja2 import Environment

from app.core.functions import PityFunction


def get_env():
    my_env = Environment()
    for func in dir(PityFunction):
        # 过滤掉内置方法
        if func.startswith("__"):
            continue
        my_env.globals[func] = getattr(PityFunction, func)
        my_env.variable_start_string = "${"
        my_env.variable_end_string = "}"
    return my_env


class Render(object):
    """
    渲染变量，用于上下文变量替换
    """
    _env = get_env()

    @staticmethod
    @lru_cache(128)
    def load(source: str):
        """
        加载模板
        :param source:
        :return:
        """
        return Render._env.from_string(source)

    @staticmethod
    def render(context: dict, source: str):
        """
        加载变量
        :param context:
        :param source:
        :return:
        """
        try:
            tmpl = Render.load(source)
            return tmpl.render(**context)
        except Exception as e:
            raise Exception(f"解析参数失败, 请检查变量是否获取到: {str(e)}")
