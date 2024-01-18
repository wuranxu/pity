"""
通过jinja2模板引擎解析上下文
"""
from functools import lru_cache

from jinja2 import Environment

from app.core.functions import PityFunction


def get_env():
    my_env = Environment()
    for func in dir(PityFunction):
        if func.startswith("__"):
            continue
        my_env.globals[func] = getattr(PityFunction, func)
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


if __name__ == "__main__":
    # import jinja2
    #
    # template = jinja2.Template("""hello {{nan.xixi[0].orderId}} """)
    #
    # from jinja2 import Environment
    # from jinja2.runtime import Context
    #
    # env = Environment()

    a = "2023-09-14 12:00:00.223"
    temp = """{{uuid()}}"""

    c = Render.render(dict(), temp)
    print(c)

    js_dat = {
        "nan": {
            "xixi": [
                {
                    "ni_zai_gan_ma": "hahahaha",
                    "orderId": 44
                }
            ]
        }
    }
