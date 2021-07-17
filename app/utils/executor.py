import json
import re
from datetime import datetime
from typing import List

from app.dao.config.GConfigDao import GConfigDao
from app.dao.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from app.dao.test_case.TestCaseDao import TestCaseDao
from app.middleware.HttpClient import Request
from app.models.test_case import TestCase
from app.utils.decorator import case_log
from app.utils.gconfig_parser import StringGConfigParser, JSONGConfigParser, YamlGConfigParser
from app.utils.logger import Log


class Executor(object):
    log = Log("Executor")
    el_exp = r"\$\{(.+?)\}"
    pattern = re.compile(el_exp)
    # 需要替换全局变量的字段
    fields = ['body', 'url', 'request_header']

    def __init__(self):
        self._logger = list()

    @property
    def logger(self):
        return self._logger

    @case_log
    def parse_gconfig(self, data: TestCase, *fields):
        """
        解析全局变量
        """
        for f in fields:
            self.parse_field(data, f)

    @case_log
    def get_parser(self, key_type):
        """获取变量解析器
        """
        if key_type == 0:
            return StringGConfigParser.parse
        if key_type == 1:
            return JSONGConfigParser.parse
        if key_type == 2:
            return YamlGConfigParser.parse
        raise Exception(f"全局变量类型: {key_type}不合法, 请检查!")

    @case_log
    def parse_field(self, data: TestCase, field):
        """
        解析字段
        """
        try:
            field_origin = getattr(data, field)
            variables = self.get_el_expression(field_origin)
            for v in variables:
                key = v.split(".")[0]
                # TODO 注意此处实时查询数据库，后续需要改成Redis
                cf = GConfigDao.get_gconfig_by_key(key)
                if cf is not None:
                    # 解析变量
                    parse = self.get_parser(cf.key_type)
                    new_value = parse(cf.value, v)
                    new_field = field_origin.replace("${%s}" % v, new_value)
                    setattr(data, field, new_field)
                    field_origin = new_field
        except Exception as e:
            Executor.log.error(f"查询全局变量失败, error: {str(e)}")
            raise

    @case_log
    def run(self, case_id: int):
        """
        开始执行测试用例
        """
        result = dict()
        try:
            case_info, err = TestCaseDao.query_test_case(case_id)
            if err:
                return result, err

            # Step1: 替换全局变量
            self.parse_gconfig(case_info, *Executor.fields)

            # 获取断言
            asserts, err = TestCaseAssertsDao.list_test_case_asserts(case_id)
            if err:
                return result, err
            if case_info.request_header != "":
                headers = json.loads(case_info.request_header)
            else:
                headers = dict()
            if "Content-Type" not in headers:
                headers['Content-Type'] = "application/json; charset=UTF-8"
            if case_info.body != '':
                body = case_info.body
            else:
                body = None
            request_obj = Request(case_info.url, headers=headers, data=body.encode())
            method = case_info.request_method.upper()
            response_info = request_obj.request(method)
            # 执行完成进行断言
            response_info["asserts"] = self.my_assert(asserts, response_info)

            # 日志输出
            response_info["logs"] = "\n".join(self.logger)
            return response_info, None
        except Exception as e:
            Executor.log.error(f"执行用例失败: {str(e)}")
            return result, f"执行用例失败: {str(e)}"

    @staticmethod
    def get_time():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @case_log
    def my_assert(self, asserts: List, response_info) -> dict:
        """
        断言验证
        """
        result = dict()
        if len(asserts) == 0:
            self.logger.append("[{}]: 未设置断言, 用例结束".format(Executor.get_time()))
            return result
        for item in asserts:
            a, err = self.parse_variable(response_info, item.expected)
            if err:
                result[item.id] = {"status": False, "msg": f"解析变量失败, {err}"}
                continue
            b, err = self.parse_variable(response_info, item.actually)
            if err:
                result[item.id] = {"status": False, "msg": f"解析变量失败, {err}"}
                continue
            try:
                a, b = self.translate(a), self.translate(b)
                status, err = self.ops(item.assert_type, a, b)
                result[item.id] = {"status": status, "msg": err}
            except Exception as e:
                result[item.id] = {"status": False, "msg": str(e)}
        return result

    @case_log
    def ops(self, assert_type: str, a, b) -> (bool, str):
        """
        通过断言类型进行校验
        """
        if assert_type == "equal":
            if a == b:
                return True, f"预期结果: {a} == 实际结果: {b}"
            return False, f"预期结果: {a} != 实际结果: {b}"
        if assert_type == "not_equal":
            if a != b:
                return True, f"预期结果: {a} != 实际结果: {b}"
            return False, f"预期结果: {a} == 实际结果: {b}"
        if assert_type == "in":
            if a in b:
                return True, f"预期结果: {a} in 实际结果: {b}"
            return False, f"预期结果: {a} in 实际结果: {b}"
        return False, "不支持的断言方式"

    @case_log
    def get_el_expression(self, string: str):
        """
        获取字符串中的el表达式
        """
        return re.findall(Executor.pattern, string)

    @case_log
    def translate(self, data):
        """
        反序列化为Python对象
        """
        return json.loads(data)

    @case_log
    def parse_variable(self, response_info, string: str):
        """
        解析返回response中的变量
        """
        data = self.get_el_expression(string)
        if len(data) == 0:
            return string, None
        data = data[0]
        el_list = data.split(".")
        # ${response.data.id}
        result = response_info
        try:
            for branch in el_list:
                if isinstance(branch, int):
                    # 说明路径里面的是数组
                    result = result[int(branch)]
                else:
                    result = result.get(branch)
        except Exception as e:
            return None, f"获取变量失败: {str(e)}"
        return json.dumps(result, ensure_ascii=False), None
