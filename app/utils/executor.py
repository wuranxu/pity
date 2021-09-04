import asyncio
import json
import re
import time
from datetime import datetime
from typing import List

from app.dao.config.GConfigDao import GConfigDao
from app.dao.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from app.dao.test_case.TestCaseDao import TestCaseDao
from app.dao.test_case.TestReport import TestReportDao
from app.dao.test_case.TestResult import TestResultDao
from app.middleware.AsyncHttpClient import AsyncRequest
from app.models.constructor import Constructor
from app.models.test_case import TestCase
from app.utils.case_logger import CaseLog
from app.utils.decorator import case_log
from app.utils.gconfig_parser import StringGConfigParser, JSONGConfigParser, YamlGConfigParser
from app.utils.logger import Log


class Executor(object):
    log = Log("Executor")
    el_exp = r"\$\{(.+?)\}"
    pattern = re.compile(el_exp)
    # 需要替换全局变量的字段
    fields = ['body', 'url', 'request_headers']

    def __init__(self, log: CaseLog = None):
        if log is None:
            self._logger = CaseLog()
            self._main = True
        else:
            self._logger = log
            self._main = False

    @property
    def logger(self):
        return self._logger

    def append(self, content, end=False):
        if end:
            self.logger.append(content)
        else:
            self.logger.append(content)

    @case_log
    async def parse_gconfig(self, data: TestCase, *fields):
        """
        解析全局变量
        """
        for f in fields:
            await self.parse_field(data, f)

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

    async def parse_field(self, data: TestCase, field):
        """
        解析字段
        """
        try:
            self.append("获取用例: [{}]字段: [{}]中的el表达式".format(data, field))
            field_origin = getattr(data, field)
            variables = self.get_el_expression(field_origin)
            for v in variables:
                key = v.split(".")[0]
                # TODO 注意此处实时查询数据库，后续需要改成Redis
                cf = await GConfigDao.async_get_gconfig_by_key(key)
                if cf is not None:
                    # 解析变量
                    parse = self.get_parser(cf.key_type)
                    new_value = parse(cf.value, v)
                    new_field = field_origin.replace("${%s}" % v, new_value)
                    setattr(data, field, new_field)
                    self.append("替换全局变量成功, 字段: [{}]:\n\n[{}] -> [{}]\n".format(field, "${%s}" % v, new_value))
                    field_origin = new_field
            self.append("获取用例字段: [{}]中的el表达式".format(field), True)
        except Exception as e:
            Executor.log.error(f"查询全局变量失败, error: {str(e)}")
            raise

    async def parse_params(self, data: TestCase, params: dict):
        self.append("正在替换变量")
        try:
            for c in data.__table__.columns:
                field_origin = getattr(data, c.name)
                if not isinstance(field_origin, str):
                    continue
                variables = self.get_el_expression(field_origin)
                for v in variables:
                    key = v.split(".")
                    if not params.get(key[0]):
                        continue
                    result = params
                    for branch in key:
                        if isinstance(result, str):
                            # 说明需要反序列化
                            try:
                                result = json.loads(result)
                            except Exception as e:
                                self.append(f"反序列化失败, result: {result}\nERROR: {e}")
                                break
                        if isinstance(branch, int):
                            # 说明路径里面的是数组
                            result = result[int(branch)]
                        else:
                            result = result.get(branch)
                    if c.name != "request_headers":
                        new_value = json.dumps(result, ensure_ascii=False)
                    else:
                        new_value = result
                        if new_value is None:
                            self.append("替换变量失败, 找不到对应的数据")
                            continue
                    new_field = field_origin.replace("${%s}" % v, new_value)
                    self.append("替换流程变量成功，字段: [{}]: \n\n[{}] -> [{}]\n".format(c.name, "${%s}" % v, new_value))
                    setattr(data, c.name, new_field)
                    field_origin = new_field
        except Exception as e:
            Executor.log.error(f"替换变量失败, error: {str(e)}")
            raise Exception(f"替换变量失败, error: {str(e)}")

    @case_log
    async def get_constructor(self, case_id):
        """获取构造数据"""
        return await TestCaseDao.async_select_constructor(case_id)

    async def execute_constructors(self, path, params, req_params, constructors: List[Constructor]):
        """开始构造数据"""
        if len(constructors) == 0:
            self.append("构造方法为空, 跳出构造环节")
        for i, c in enumerate(constructors):
            await self.execute_constructor(i, path, params, req_params, c)

    async def execute_constructor(self, index, path, params, req_params, constructor: Constructor):
        if not constructor.enable:
            self.append(f"当前路径: {path}, 构造方法: {constructor.name} 已关闭, 不继续执行")
            return
        if constructor.type == 0:
            data = json.loads(constructor.constructor_json)
            case_id = data.get("case_id")
            testcase, _ = await TestCaseDao.async_query_test_case(case_id)
            try:
                self.append(f"当前路径: {path}, 第{index + 1}条构造方法")
                # 说明是case
                executor = Executor(self.logger)
                new_param = data.get("params")
                if new_param:
                    temp = json.loads(new_param)
                    req_params.update(temp)
                result, err = await executor.run(case_id, params, req_params, f"{path}->{testcase.name}")
                if err:
                    raise Exception(err)
                params[constructor.value] = result
                await self.parse_params(testcase, params)
            except Exception as e:
                raise Exception(f"{path}->{testcase.name} 第{index + 1}个构造方法执行失败: {e}")

    async def run(self, case_id: int, params_pool: dict = None, request_param: dict = None, path="主case"):
        """
        开始执行测试用例
        """
        response_info = dict()

        # 初始化case全局变量, 只存在于case生命周期 注意 它与全局变量不是一套逻辑
        case_params = params_pool
        if case_params is None:
            case_params = dict()

        req_params = request_param
        if req_params is None:
            req_params = dict()

        try:
            case_info, err = await TestCaseDao.async_query_test_case(case_id)
            if err:
                return response_info, err

            response_info["case_name"] = case_info.name
            method = case_info.request_method.upper()
            response_info["request_method"] = method

            # Step1: 替换全局变量
            await self.parse_gconfig(case_info, *Executor.fields)

            self.append("解析全局变量", True)

            # Step2: 获取构造数据
            constructors = await self.get_constructor(case_id)

            # Step3: 执行构造方法
            await self.execute_constructors(path, case_params, req_params, constructors)

            # Step4: 获取断言
            asserts, err = await TestCaseAssertsDao.async_list_test_case_asserts(case_id)

            response_info["url"] = case_info.url

            if err:
                return response_info, err

            # Step5: 获取后置操作
            # TODO

            # Step6: 批量改写主方法参数
            await self.parse_params(case_info, case_params)

            if case_info.request_headers != "":
                headers = json.loads(case_info.request_headers)
            else:
                headers = dict()
            if "Content-Type" not in headers:
                headers['Content-Type'] = "application/json; charset=UTF-8"
            if case_info.body != '':
                body = case_info.body
            else:
                body = None

            # Step5: 替换请求参数
            body = self.replace_body(request_param, body)

            # Step6: 完成http请求

            if "form" not in headers['Content-Type']:
                request_obj = AsyncRequest(case_info.url, headers=headers,
                                           data=body.encode() if body is not None else body)
            else:
                if body is not None:
                    body = json.loads(body)
                request_obj = AsyncRequest(case_info.url, headers=headers, data=body)
            res = await request_obj.invoke(method)
            response_info.update(res)
            # 执行完成进行断言
            response_info["asserts"] = self.my_assert(asserts, response_info)
            # 日志输出, 如果不是开头用例则不记录
            if self._main:
                response_info["logs"] = self.logger.join()
            return response_info, None
        except Exception as e:
            Executor.log.error(f"执行用例失败: {str(e)}")
            return response_info, f"执行用例失败: {str(e)}"

    @staticmethod
    async def run_single(data, report_id, case_id, params_pool: dict = None, request_param: dict = None,
                         path="主case"):
        start_at = datetime.now()
        executor = Executor()
        result, err = await executor.run(case_id, params_pool, request_param, path)
        finished_at = datetime.now()
        cost = "{}s".format((finished_at - start_at).seconds)
        if err is not None:
            status = 2
        else:
            if result.get("status"):
                status = 0
            else:
                status = 1
        asserts = result.get("asserts")
        url = result.get("url")
        case_logs = result.get("logs")
        body = result.get("request_data")
        status_code = result.get("status_code")
        request_method = result.get("request_method")
        request_headers = result.get("request_headers")
        response = result.get("response")
        case_name = result.get("case_name")
        response_headers = result.get("response_headers")
        cookies = result.get("cookies")
        data[case_id] = status
        await TestResultDao.insert(report_id, case_id, case_name, status,
                                   case_logs, start_at, finished_at,
                                   url, body, request_method, request_headers, cost,
                                   asserts, response_headers, response,
                                   status_code, cookies, 0)

    @case_log
    def replace_body(self, req_params, body):
        """根据传入的构造参数进行参数替换"""
        try:
            if body:
                data = json.loads(body)
                for k, v in req_params.items():
                    if data.get(k) is not None:
                        data[k] = v
                return json.dumps(data, ensure_ascii=False)
            self.append(f"body为空, 不进行替换")
        except Exception as e:
            self.append(f"替换请求body失败, {e}")
        return body

    @staticmethod
    def get_time():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @case_log
    def my_assert(self, asserts: List, response_info) -> str:
        """
        断言验证
        """
        result = dict()
        if len(asserts) == 0:
            self.append("未设置断言, 用例结束")
            return json.dumps(result, ensure_ascii=False)
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
        return json.dumps(result, ensure_ascii=False)

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

    def get_el_expression(self, string: str):
        """获取字符串中的el表达式
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
                if isinstance(result, str):
                    # 说明需要反序列化
                    try:
                        result = json.loads(result)
                    except Exception as e:
                        self.append(f"反序列化失败, result: {result}\nERROR: {e}")
                        break
                if isinstance(branch, int):
                    # 说明路径里面的是数组
                    result = result[int(branch)]
                else:
                    result = result.get(branch)
        except Exception as e:
            return None, f"获取变量失败: {str(e)}"
        return json.dumps(result, ensure_ascii=False), None

    @staticmethod
    async def run_multiple(executor: int, env: int, case_list: List[int]):
        st = time.perf_counter()
        # step1: 新增测试报告数据
        report_id = await TestReportDao.start(executor, env)
        # step2: 开始执行用例
        result_data = dict()
        # step3: 将报告改为 running状态
        await TestReportDao.update(report_id, 1)
        # step4: 并发执行用例并搜集数据
        await asyncio.gather(*(Executor.run_single(result_data, report_id, c) for c in case_list))
        ok, fail, skip, error = 0, 0, 0, 0
        for case_id, status in result_data.items():
            if status == 0:
                ok += 1
            elif status == 1:
                fail += 1
            elif status == 2:
                error += 1
            else:
                skip += 1
        cost = time.perf_counter() - st
        cost = "%.2f" % cost
        # step5: 回写数据到报告
        await TestReportDao.end(report_id, ok, fail, error, skip, 3, cost)
        return report_id
