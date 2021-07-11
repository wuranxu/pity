__author__ = "woody"

import json

import yaml

from app.utils.logger import Log

"""
全局变量解析器，包括JSON/YAML/STRING
"""


class GConfigParser(object):
    log = Log("GConfigParser")

    @staticmethod
    def parse(value, jsonpath):
        pass

    @staticmethod
    def get(data, key):
        el_list = key.split(".")
        result = data
        try:
            for branch in el_list[1:]:
                if isinstance(branch, int):
                    # 说明路径里面的是数组
                    result = result[int(branch)]
                else:
                    result = result.get(branch)
        except Exception as e:
            GConfigParser.log.error(f"解析data: {data} key: {key} 数据失败: {e}")
            return None
        if not isinstance(result, str):
            return json.dumps(result, ensure_ascii=False)
        return result


class YamlGConfigParser(GConfigParser):

    @staticmethod
    def get_data(value):
        return yaml.safe_load(value)

    @staticmethod
    def parse(value, jsonpath):
        try:
            data = YamlGConfigParser.get_data(value)
            return GConfigParser.get(data, jsonpath)
        except Exception as e:
            GConfigParser.log.error(f"解析YAML全局变量异常: {e}")
            return None


class StringGConfigParser(GConfigParser):

    def parse(self, value, jsonpath):
        return value


class JSONGConfigParser(GConfigParser):
    @staticmethod
    def get_data(value):
        return json.loads(value)

    @staticmethod
    def parse(value, jsonpath):
        try:
            data = JSONGConfigParser.get_data(value)
            return GConfigParser.get(data, jsonpath)
        except Exception as e:
            GConfigParser.log.error(f"解析JSON全局变量异常: {e}")
            return None
