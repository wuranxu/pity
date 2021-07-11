import json
import re
from typing import List

from app.dao.config.GConfigDao import GConfigDao
from app.dao.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from app.dao.test_case.TestCaseDao import TestCaseDao
from app.middleware.HttpClient import Request
from app.models.test_case import TestCase
from app.utils.gconfig_parser import StringGConfigParser, JSONGConfigParser, YamlGConfigParser
from app.utils.logger import Log


class Executor(object):
    log = Log("Executor")
    el_exp = r"\$\{(.+)\}"
    pattern = re.compile(el_exp)
    # 需要替换全局变量的字段
    fields = ['body', 'url', 'request_header']

    @staticmethod
    def parse_gconfig(data: TestCase, *fields):
        for f in fields:
            Executor.parse_field(data, f)

    @staticmethod
    def get_parser(key_type):
        if key_type == 0:
            return StringGConfigParser.parse
        if key_type == 1:
            return JSONGConfigParser.parse
        if key_type == 2:
            return YamlGConfigParser.parse
        raise Exception(f"全局变量类型: {key_type}不合法, 请检查!")

    @staticmethod
    def parse_field(data: TestCase, field):
        try:
            field_origin = getattr(data, field)
            variables = Executor.get_el_expression(field_origin)
            for v in variables:
                key = v.split(".")[0]
                # TODO 注意此处实时查询数据库，后续需要改成Redis
                cf = GConfigDao.get_gconfig_by_key(key)
                if cf is not None:
                    # 解析变量
                    parse = Executor.get_parser(cf.key_type)
                    new_value = parse(cf.value, v)
                    new_field = field_origin.replace("${%s}" % v, new_value)
                    setattr(data, field, new_field)
                    field_origin = new_field
        except Exception as e:
            Executor.log.error(f"查询全局变量失败, error: {str(e)}")
            raise

    @staticmethod
    def run(case_id: int):
        result = dict()
        try:
            case_info, err = TestCaseDao.query_test_case(case_id)
            if err:
                return result, err

            # Step1: 替换全局变量
            Executor.parse_gconfig(case_info, *Executor.fields)

            # 获取断言
            asserts, err = TestCaseAssertsDao.list_test_case_asserts(case_id)
            if err:
                return result, err
            if case_info.request_header != "":
                headers = json.loads(case_info.request_header)
            else:
                headers = dict()
            if case_info.body != '':
                body = case_info.body
            else:
                body = None
            request_obj = Request(case_info.url, headers=headers, data=body.encode())
            method = case_info.request_method.upper()
            response_info = request_obj.request(method)
            # 执行完成进行断言
            response_info["asserts"] = Executor.my_assert(asserts, response_info)
            return response_info, None
        except Exception as e:
            Executor.log.error(f"执行用例失败: {str(e)}")
            return result, f"执行用例失败: {str(e)}"

    @staticmethod
    def my_assert(asserts: List, response_info):
        result = dict()
        for item in asserts:
            a, err = Executor.parse_variable(response_info, item.expected)
            if err:
                result[item.id] = {"status": False, "msg": f"解析变量失败, {err}"}
                continue
            b, err = Executor.parse_variable(response_info, item.actually)
            if err:
                result[item.id] = {"status": False, "msg": f"解析变量失败, {err}"}
                continue
            try:
                a, b = Executor.translate(a), Executor.translate(b)
                status, err = Executor.ops(item.assert_type, a, b)
                result[item.id] = {"status": status, "msg": err}
            except Exception as e:
                result[item.id] = {"status": False, "msg": str(e)}
        return result

    @staticmethod
    def ops(assert_type: str, a, b) -> (bool, str):
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

    @staticmethod
    def get_el_expression(string: str):
        """
        获取el表达式
        :param string:
        :return:
        """
        return re.findall(Executor.pattern, string)

    @staticmethod
    def translate(data):
        return json.loads(data)

    @staticmethod
    def parse_variable(response_info, string: str):
        data = Executor.get_el_expression(string)
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
