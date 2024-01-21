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
        raise NotImplementedError

    @staticmethod
    def get_data(value):
        raise NotImplementedError

    @staticmethod
    def get(data, key):
        el_list = key.split(".")
        result = data
        try:
            for branch in el_list[1:]:
                if isinstance(result, str):
                    # 说明需要反序列化
                    try:
                        result = json.loads(result)
                    except Exception as e:
                        raise Exception(f"反序列化失败, result: {result}\nERROR: {e}")
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
        """Yaml解析器"""
        try:
            data = YamlGConfigParser.get_data(value)
            return GConfigParser.get(data, jsonpath)
        except Exception as e:
            GConfigParser.log.error(f"解析YAML全局变量异常: {e}")
            return None


class StringGConfigParser(GConfigParser):

    @staticmethod
    def parse(value, jsonpath):
        """String解析器"""
        return value

    @staticmethod
    def get_data(value):
        return value


class JSONGConfigParser(GConfigParser):
    @staticmethod
    def get_data(value):
        return json.loads(value)

    @staticmethod
    def parse(value, jsonpath):
        """JSON解析器"""
        try:
            data = JSONGConfigParser.get_data(value)
            return GConfigParser.get(data, jsonpath)
        except Exception as e:
            GConfigParser.log.error(f"解析JSON全局变量异常: {e}")
            return None
