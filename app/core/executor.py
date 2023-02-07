import asyncio
import json
import re
import time
from collections import defaultdict
from datetime import datetime
from typing import List, Any

from app.core.constructor.case_constructor import TestcaseConstructor
from app.core.constructor.http_constructor import HttpConstructor
from app.core.constructor.python_constructor import PythonConstructor
from app.core.constructor.redis_constructor import RedisConstructor
from app.core.constructor.sql_constructor import SqlConstructor
from app.core.msg.dingtalk import DingTalk
from app.core.msg.mail import Email
from app.core.paramters import parameters_parser
from app.core.ws_connection_manager import ws_manage
from app.crud.auth.UserDao import UserDao
from app.crud.config.AddressDao import PityGatewayDao
from app.crud.config.EnvironmentDao import EnvironmentDao
from app.crud.config.GConfigDao import GConfigDao
from app.crud.project.ProjectDao import ProjectDao
from app.crud.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from app.crud.test_case.TestCaseDao import TestCaseDao
from app.crud.test_case.TestCaseOutParametersDao import PityTestCaseOutParametersDao
from app.crud.test_case.TestPlan import PityTestPlanDao
from app.crud.test_case.TestReport import TestReportDao
from app.crud.test_case.TestResult import TestResultDao
from app.crud.test_case.TestcaseDataDao import PityTestcaseDataDao
from app.enums.ConstructorEnum import ConstructorType
from app.enums.GconfigEnum import GConfigParserEnum, GconfigType
from app.enums.NoticeEnum import NoticeType
from app.enums.RequestBodyEnum import BodyType
from app.middleware.AsyncHttpClient import AsyncRequest
from app.models.constructor import Constructor
from app.models.out_parameters import PityTestCaseOutParameters
from app.models.project import Project
from app.models.test_case import TestCase
from app.models.test_plan import PityTestPlan
from app.models.testcase_asserts import TestCaseAsserts
from app.utils.case_logger import CaseLog
from app.utils.decorator import case_log, lock
from app.utils.gconfig_parser import StringGConfigParser, JSONGConfigParser, YamlGConfigParser
from app.utils.json_compare import JsonCompare
from app.utils.logger import Log
from config import Config


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

    @staticmethod
    def get_constructor_type(c: Constructor):
        if c.type == ConstructorType.testcase:
            return TestcaseConstructor
        if c.type == ConstructorType.sql:
            return SqlConstructor
        if c.type == ConstructorType.redis:
            return RedisConstructor
        if c.type == ConstructorType.py_script:
            return PythonConstructor
        if c.type == ConstructorType.http:
            return HttpConstructor
        return None

    def append(self, content, end=False):
        if end:
            self.logger.append(content, end)
        else:
            self.logger.append(content, end)

    @case_log
    async def parse_gconfig(self, data, type_, env, *fields):
        """
        解析全局变量
        """
        for f in fields:
            await self.parse_field(data, f, GconfigType.text(type_), env)

    @case_log
    def get_parser(self, key_type):
        """获取变量解析器
        """
        if key_type == GConfigParserEnum.string:
            return StringGConfigParser.parse
        if key_type == GConfigParserEnum.json:
            return JSONGConfigParser.parse
        if key_type == GConfigParserEnum.yaml:
            return YamlGConfigParser.parse
        raise Exception(f"全局变量类型: {key_type}不合法, 请检查!")

    async def parse_field(self, data, field, name, env):
        """
        解析字段
        """
        try:
            self.append("获取{}: [{}]字段: [{}]中的el表达式".format(name, data, field))
            field_origin = getattr(data, field)
            variables = self.get_el_expression(field_origin)
            for v in variables:
                key = v.split(".")[0]
                cf = await GConfigDao.async_get_gconfig_by_key(key, env)
                if cf is not None:
                    # 解析变量
                    parse = self.get_parser(cf.key_type)
                    new_value = parse(cf.value, v)
                    new_field = field_origin.replace("${%s}" % v, new_value)
                    setattr(data, field, new_field)
                    self.append("替换全局变量成功, 字段: [{}]:\n\n[{}] -> [{}]\n".format(field, "${%s}" % v, new_value))
                    field_origin = new_field
            self.append("获取{}字段: [{}]中的el表达式".format(name, field), True)
        except Exception as e:
            Executor.log.error(f"查询全局变量失败, error: {str(e)}")
            raise Exception(f"查询全局变量失败, error: {str(e)}")

    def replace_params(self, field_name, field_origin, params: dict):
        new_data = dict()
        if not isinstance(field_origin, str):
            return new_data
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
                if branch.isdigit():
                    # 说明路径里面的是数组
                    result = result[int(branch)]
                else:
                    result = result.get(branch)
                if result is None:
                    raise Exception(f"变量路径: {v}不存在, 请检查JSON或路径!")
            if field_name == "request_headers":
                new_value = json.loads(result)
            elif not isinstance(result, str):
                new_value = json.dumps(result, ensure_ascii=False)
            else:
                new_value = result
                if new_value is None:
                    self.append("替换变量失败, 找不到对应的数据")
                    continue
            new_data["${%s}" % v] = new_value
        return new_data

    async def parse_params(self, data: TestCase, params: dict):
        self.append("正在替换变量")
        try:
            for c in data.__table__.columns:
                field_origin = getattr(data, c.name)
                replace_kv = self.replace_params(c.name, field_origin, params)
                for k, v in replace_kv.items():
                    new_field = field_origin.replace(k, v)
                    setattr(data, c.name, new_field)
                    self.append("替换流程变量成功，字段: [{}]: \n\n[{}] -> [{}]\n".format(c.name, k, v))
        except Exception as e:
            Executor.log.error(f"替换变量失败, error: {str(e)}")
            raise Exception(f"替换变量失败, error: {str(e)}")

    @case_log
    async def get_constructor(self, case_id):
        """获取构造数据"""
        return await TestCaseDao.async_select_constructor(case_id)

    async def execute_constructors(self, env: int, path, case_info, params, req_params, constructors: List[Constructor],
                                   asserts, suffix=False):
        """开始构造数据"""
        if len(constructors) == 0:
            self.append("前后置条件为空, 跳出该环节")
        current = 0
        for i, c in enumerate(constructors):
            if c.suffix == suffix:
                await self.execute_constructor(env, current, path, params, req_params, c)
                self.replace_args(params, case_info, constructors, asserts)
                current += 1

    async def execute_constructor(self, env, index, path, params, req_params, constructor: Constructor):
        if not constructor.enable:
            self.append(f"当前路径: {path}, 构造方法: {constructor.name} 已关闭, 不继续执行")
            return False
        construct = Executor.get_constructor_type(constructor)
        if construct is None:
            self.append(f"构造方法类型: {constructor.type} 不合法, 请检查")
            return
        await construct.run(self, env, index, path, params, req_params, constructor, executor_class=Executor)

    # async def execute_constructor(self, env, index, path, params, req_params, constructor: Constructor):
    #     if not constructor.enable:
    #         self.append(f"当前路径: {path}, 构造方法: {constructor.name} 已关闭, 不继续执行")
    #         return
    #     if constructor.type == 0:
    #         try:
    #             data = json.loads(constructor.constructor_json)
    #             case_id = data.get("case_id")
    #             testcase, _ = await TestCaseDao.async_query_test_case(case_id)
    #             self.append(f"当前路径: {path}, 第{index + 1}条构造方法")
    #             # 说明是case
    #             executor = Executor(self.logger)
    #             new_param = data.get("params")
    #             if new_param:
    #                 temp = json.loads(new_param)
    #                 req_params.update(temp)
    #             result, err = await executor.run(env, case_id, params, req_params, f"{path}->{testcase.name}")
    #             if err:
    #                 raise Exception(err)
    #             if not result["status"]:
    #                 raise Exception(f"断言失败, 断言数据: {result.get('asserts', 'unknown')}")
    #             params[constructor.value] = result
    #             # await self.parse_params(testcase, params)
    #         except Exception as e:
    #             raise Exception(f"{path}->{constructor.name} 第{index + 1}个构造方法执行失败: {e}")
    #     elif constructor.type == 1:
    #         # 说明是sql语句
    #         try:
    #             self.append(f"当前路径: {path}, 第{index + 1}条构造方法")
    #             data = json.loads(constructor.constructor_json)
    #             database = data.get("database")
    #             sql = data.get("sql")
    #             self.append(f"当前构造方法类型为sql, 数据库名: {database}\nsql: {sql}\n")
    #             sql_data = await DbConfigDao.execute_sql(env, database, sql)
    #             params[constructor.value] = sql_data
    #             self.append(f"当前构造方法返回变量: {constructor.value}\n返回值:\n {sql_data}\n")
    #         except Exception as e:
    #             raise Exception(f"{path}->{constructor.name} 第{index + 1}个构造方法执行失败: {e}")

    def add_header(self, case_info, headers):
        """
        @ desperate
        :param case_info:
        :param headers:
        :return:
        """
        if case_info.body_type == BodyType.none:
            return
        if case_info.body_type == BodyType.json:
            if "Content-Type" not in headers:
                headers['Content-Type'] = "application/json; charset=UTF-8"

    @case_log
    def extract_out_parameters(self, response_info, data: List[PityTestCaseOutParameters]):
        """提取出参数据"""
        result = dict()
        for d in data:
            p = parameters_parser(d.source)
            result[d.name] = p(response_info, d.expression, idx=d.match_index)
        return result

    async def run(self, env: int, case_id: int, params_pool: dict = None, request_param: dict = None, path="主case"):
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
            response_info['case_id'] = case_info.id
            response_info["case_name"] = case_info.name
            method = case_info.request_method.upper()
            response_info["request_method"] = method

            # Step1: 替换全局变量
            await self.parse_gconfig(case_info, GconfigType.case, env, *Executor.fields)

            self.append("解析全局变量", True)

            # Step2: 获取构造数据
            constructors = await self.get_constructor(case_id)

            #  Step3: 解析前后置条件的全局变量
            for c in constructors:
                await self.parse_gconfig(c, GconfigType.constructor, env, "constructor_json")

            # Step4: 获取断言
            asserts = await TestCaseAssertsDao.async_list_test_case_asserts(case_id)

            # 获取出参信息
            out_parameters = await PityTestCaseOutParametersDao.select_list(case_id=case_id)

            for ast in asserts:
                await self.parse_gconfig(ast, GconfigType.asserts, env, "expected", "actually")

            # Step5: 替换参数
            self.replace_args(req_params, case_info, constructors, asserts)

            # Step6: 执行前置条件
            await self.execute_constructors(env, path, case_info, case_params, req_params, constructors, asserts)

            # Step7: 批量改写主方法参数
            await self.parse_params(case_info, case_params)

            if case_info.request_headers and case_info.request_headers != "":
                headers = json.loads(case_info.request_headers)
            else:
                headers = dict()

            body = case_info.body if case_info.body != '' else None

            # Step8: 替换请求参数
            body = self.replace_body(request_param, body, case_info.body_type)

            # Step9: 替换base_path
            if case_info.base_path:
                base_path = await PityGatewayDao.query_gateway(env, case_info.base_path)
                case_info.url = f"{base_path}{case_info.url}"

            response_info["url"] = case_info.url

            # Step9: 完成http请求
            request_obj = await AsyncRequest.client(url=case_info.url, body_type=case_info.body_type, headers=headers,
                                                    body=body)
            res = await request_obj.invoke(method)
            self.append(f"http请求过程\n\nRequest Method: {case_info.request_method}\n\n"
                        f"Request Headers:\n{headers}\n\nUrl: {case_info.url}"
                        f"\n\nBody:\n{body}\n\nResponse:\n{res.get('response', '未获取到返回值')}")
            response_info.update(res)

            # 提取出参
            out_dict = self.extract_out_parameters(response_info, out_parameters)

            # 替换主变量
            case_params.update(out_dict)

            # 写入response
            # TODO
            # req_params["response"] = res.get("response", "")

            self.replace_asserts(req_params, asserts)
            self.replace_constructors(req_params, constructors)

            # Step10: 执行后置条件
            await self.execute_constructors(env, path, case_info, case_params, req_params, constructors, asserts, True)

            # Step11: 断言
            asserts, ok = self.my_assert(asserts, response_info.get('json_format'))
            response_info["status"] = ok
            response_info["asserts"] = asserts
            # 日志输出, 如果不是主用例则不记录
            if self._main:
                response_info["logs"] = self.logger.join()
            return response_info, None
        except Exception as e:
            Executor.log.exception("执行用例失败: \n")
            self.append(f"执行用例失败: {str(e)}")
            if self._main:
                response_info["logs"] = self.logger.join()
            return response_info, f"执行用例失败: {str(e)}"

    @staticmethod
    def get_dict(json_data: str):
        return json.loads(json_data)

    def replace_cls(self, params: dict, cls, *fields: Any):
        for k, v in params.items():
            for f in fields:
                fd = getattr(cls, f, '')
                if fd is None:
                    continue
                if k in fd:
                    data = self.replace_params(f, fd, params)
                    for a, b in data.items():
                        fd = fd.replace(a, b)
                        setattr(cls, f, fd)

    def replace_args(self, params, data: TestCase, constructors: List[Constructor], asserts: List[TestCaseAsserts]):
        self.replace_testcase(params, data)
        self.replace_constructors(params, constructors)
        self.replace_asserts(params, asserts)

    def replace_testcase(self, params: dict, data: TestCase):
        """替换测试用例中的参数"""
        self.replace_cls(params, data, "request_headers", "body", "url")

    def replace_constructors(self, params: dict, constructors: List[Constructor]):
        """替换数据构造器中的参数"""
        for c in constructors:
            self.replace_cls(params, c, "constructor_json")

    def replace_asserts(self, params, asserts: List[TestCaseAsserts]):
        """替换断言中的参数"""
        for a in asserts:
            self.replace_cls(params, a, "expected", "actually")

    @staticmethod
    async def run_with_test_data(env, data, report_id, case_id, params_pool: dict = None, request_param: dict = None,
                                 path='主case', name: str = "", data_id: int = None, retry_minutes: int = 0):
        retry_times = Config.RETRY_TIMES if retry_minutes > 0 else 0
        times = 0
        for i in range(retry_times + 1):
            start_at = datetime.now()
            executor = Executor()
            result, err = await executor.run(env, case_id, params_pool, request_param, path)
            finished_at = datetime.now()
            cost = "{}s".format((finished_at - start_at).seconds)
            if err is not None:
                status = 2
            else:
                status = 0 if result.get("status") else 1
            # 若status不为0，代表case执行失败，走重试逻辑
            if status != 0 and i < retry_times:
                await asyncio.sleep(60 * retry_minutes)
                times += 1
                continue
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
            req = json.dumps(request_param, ensure_ascii=False)
            data[case_id].append(status)
            await TestResultDao.insert_report(report_id, case_id, case_name, status,
                                              case_logs, start_at, finished_at,
                                              url, body, request_method, request_headers, cost,
                                              asserts, response_headers, response,
                                              status_code, cookies, times, req, name, data_id)
            break

    @staticmethod
    async def run_single(env: int, data, report_id, case_id, params_pool: dict = None, path="主case", retry_minutes=0):
        test_data = await PityTestcaseDataDao.list_testcase_data_by_env(env, case_id)
        if not test_data:
            await Executor.run_with_test_data(env, data, report_id, case_id, params_pool, dict(), path,
                                              "默认数据", retry_minutes=retry_minutes)
        else:
            await asyncio.gather(
                *(Executor.run_with_test_data(env, data, report_id, case_id, params_pool,
                                              Executor.get_dict(x.json_data),
                                              path, x.name, x.id, retry_minutes=retry_minutes)
                  for x in test_data))

    @case_log
    def replace_body(self, req_params, body, body_type=1):
        """根据传入的构造参数进行参数替换"""
        if body_type != BodyType.json:
            self.append("当前请求数据不为json, 跳过替换")
            return body
        try:
            if body:
                data = json.loads(body)
                if req_params is not None:
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
    def my_assert(self, asserts: List, json_format: bool) -> [str, bool]:
        """
        断言验证
        """
        result = dict()
        ok = True
        if len(asserts) == 0:
            self.append("未设置断言, 用例结束")
            return json.dumps(result, ensure_ascii=False), ok
        for item in asserts:
            try:
                # 解析预期/实际结果
                expected = self.translate(item.expected)
                # 判断请求返回是否是json格式，如果不是则不进行loads操作
                actually = self.translate(item.actually)
                status, err = self.ops(item.assert_type, expected, actually)
                if not status:
                    ok = False
                result[item.id] = {"status": status, "msg": err}
            except Exception as e:
                ok = False
                self.append(f"预期结果: {item.expected}\n实际结果: {item.actually}\n")
                result[item.id] = {"status": False, "msg": f"断言取值失败, 请检查断言语句: {e}"}
        return json.dumps(result, ensure_ascii=False), ok

    @case_log
    def ops(self, assert_type: str, exp, act) -> (bool, str):
        """
        通过断言类型进行校验
        """
        if assert_type == "equal":
            if exp == act:
                return True, f"预期结果: {exp} 等于 实际结果: {act}【✔】"
            return False, f"预期结果: {exp} 不等于 实际结果: {act}【❌】"
        if assert_type == "not_equal":
            if exp != act:
                return True, f"预期结果: {exp} 不等于 实际结果: {act}【✔】"
            return False, f"预期结果: {exp} 等于 实际结果: {act}【❌】"
        if assert_type == "in":
            if exp in act:
                return True, f"预期结果: {exp} 包含于 实际结果: {act}【✔】"
            return False, f"预期结果: {exp} 不包含于 实际结果: {act}【❌】"
        if assert_type == "not_in":
            if exp not in act:
                return True, f"预期结果: {exp} 不包含于 实际结果: {act}【✔】"
            return False, f"预期结果: {exp} 包含于 实际结果: {act}【❌】"
        if assert_type == "contain":
            if act in exp:
                return True, f"预期结果: {exp} 包含 实际结果: {act}【✔】"
            return False, f"预期结果: {exp} 不包含 实际结果: {act}【❌】"
        if assert_type == "not_contain":
            if act not in exp:
                return True, f"预期结果: {exp} 不包含 实际结果: {act}【✔】"
            return False, f"预期结果: {exp} 包含 实际结果: {act}【❌】"
        if assert_type == "length_eq":
            if exp == len(act):
                return True, f"预期数量: {exp} 等于 实际数量: {len(act)}【✔】"
            return False, f"预期数量: {exp} 不等于 实际数量: {len(act)}【❌】"
        if assert_type == "length_gt":
            if exp > len(act):
                return True, f"预期数量: {exp} 大于 实际数量: {len(act)}【✔】"
            return False, f"预期数量: {exp} 不大于 实际数量: {len(act)}【❌】"
        if assert_type == "length_ge":
            if exp >= len(act):
                return True, f"预期数量: {exp} 大于等于 实际数量: {len(act)}【✔】"
            return False, f"预期数量: {exp} 小于 实际数量: {len(act)}【❌】"
        if assert_type == "length_le":
            if exp <= len(act):
                return True, f"预期数量: {exp} 小于等于 实际数量: {len(act)}【✔】"
            return False, f"预期数量: {exp} 大于 实际数量: {len(act)}【❌】"
        if assert_type == "length_lt":
            if exp < len(act):
                return True, f"预期数量: {exp} 小于 实际数量: {len(act)}【✔】"
            return False, f"预期数量: {exp} 不小于 实际数量: {len(act)}【❌】"
        if assert_type == "json_equal":
            data = JsonCompare().compare(exp, act)
            if len(data) == 0:
                return True, "预期JSON 等于 实际JSON【✔】"
            return False, data
        if assert_type == "text_in":
            if isinstance(act, str):
                # 如果b是string，则不转换
                if exp in act:
                    return True, f"预期结果: {exp} 文本包含于 实际结果: {act}【✔】"
                return False, f"预期结果: {exp} 文本不包含于 实际结果: {act}【❌】"
            temp = json.dumps(act, ensure_ascii=False)
            if exp in temp:
                return True, f"预期结果: {exp} 文本包含于 实际结果: {act}【✔】"
            return False, f"预期结果: {exp} 文本不包含于 实际结果: {act}【❌】"
        if assert_type == "text_not_in":
            if isinstance(act, str):
                if exp in act:
                    return True, f"预期结果: {exp} 文本包含于 实际结果: {act}【❌】"
                return False, f"预期结果: {exp} 文本不包含于 实际结果: {act}【✔】"
            temp = json.dumps(act, ensure_ascii=False)
            if exp in temp:
                return True, f"预期结果: {exp} 文本包含于 实际结果: {act}【❌】"
            return False, f"预期结果: {exp} 文本不包含于 实际结果: {act}【✔】"
        return False, "不支持的断言方式💔"

    def get_el_expression(self, string: str):
        """获取字符串中的el表达式
        """
        if string is None:
            return []
        return re.findall(Executor.pattern, string)

    @case_log
    def translate(self, data):
        """
        反序列化为Python对象
        """
        return json.loads(data)

    def replace_branch(self, branch: str, params: dict):
        if not params:
            return branch
        if branch.startswith("#"):
            # 说明branch也是个子变量
            data = branch[1:]
            if len(data) == 0:
                return branch
            dist = params.get(data)
            if dist is None:
                return branch
            return params.get(data)
        return branch

    @case_log
    def parse_variable(self, response_info, string: str, params=None):
        """
        解析返回response中的变量
        """
        exp = self.get_el_expression(string)
        if len(exp) == 0:
            return string
        data = exp[0]
        el_list = data.split(".")
        # ${response.data.id}
        result = response_info
        try:
            for branch in el_list:
                branch = self.replace_branch(branch, params)
                if isinstance(result, str):
                    # 说明需要反序列化
                    try:
                        result = json.loads(result)
                    except Exception as e:
                        self.append(f"反序列化失败, result: {result}\nERROR: {e}")
                        break
                # 2022-02-27 修复数组变量替换的bug
                if isinstance(branch, int) or branch.isdigit():
                    # 说明路径里面的是数组
                    result = result[int(branch)]
                else:
                    result = result.get(branch)
        except Exception as e:
            raise Exception(f"获取变量失败: {str(e)}")
        if string == "${response}":
            return result
        return json.dumps(result, ensure_ascii=False)

    @staticmethod
    async def notice(env: list, plan: PityTestPlan, project: Project, report_dict: dict, users: list):
        """
        消息通知方法
        :param env:
        :param plan:
        :param project:
        :param report_dict:
        :param users:
        :return:
        """
        for e in env:
            msg_types = plan.msg_type.split(",")
            if msg_types and users:
                for m in msg_types:
                    if int(m) == NoticeType.EMAIL:
                        render_html = Email.render_html(plan_name=plan.name, **report_dict[e])
                        await Email.send_msg(
                            f"【{report_dict[e].get('env')}】测试计划【{plan.name}】执行完毕（{report_dict[e].get('plan_result')}）",
                            render_html, None, *[r.get("email") for r in users])
                    if int(m) == NoticeType.DINGDING:
                        report_dict[e]['result_color'] = '#67C23A' if report_dict[e]['plan_result'] == '通过' \
                            else '#E6A23C'
                        # 批量获取用户手机号
                        users = [r.get("phone") for r in users]
                        report_dict[e]['notification_user'] = " ".join(map(lambda x: f"@{x}", users))
                        render_markdown = DingTalk.render_markdown(**report_dict[e], plan_name=plan.name)
                        if not project.dingtalk_url:
                            Executor.log.debug("项目未配置钉钉通知机器人")
                            continue
                        ding = DingTalk(project.dingtalk_url)
                        await ding.send_msg("pity测试报告", render_markdown, None, users,
                                            link=report_dict[e]['report_url'])

    @staticmethod
    @lock("test_plan")
    async def run_test_plan(plan_id: int, executor: int = 0):
        """
        通过测试计划id执行测试计划
        :param plan_id:
        :param executor:
        :return:
        """
        plan = await PityTestPlanDao.query_test_plan(plan_id)
        if plan is None:
            Executor.log.debug(f"测试计划: [{plan_id}]不存在")
            return
        try:
            # 设置为running
            await PityTestPlanDao.update_test_plan_state(plan.id, 1)
            project, _ = await ProjectDao.query_project(plan.project_id)
            env = list(map(int, plan.env.split(",")))
            case_list = list(map(int, plan.case_list.split(",")))
            receiver = list(map(int, plan.receiver.split(",") if plan.receiver else []))
            # 聚合报告dict
            report_dict = dict()
            await asyncio.gather(
                *(Executor.run_multiple(executor, int(e), case_list, mode=1, retry_minutes=plan.retry_minutes,
                                        plan_id=plan.id, ordered=plan.ordered, report_dict=report_dict) for e in env))
            await PityTestPlanDao.update_test_plan_state(plan.id, 0)
            users = await UserDao.list_user_touch(*receiver)
            await Executor.notice(env, plan, project, report_dict, users)
            if executor != 0:
                await ws_manage.notify(executor, title="测试计划执行完毕", content=f"请前往测试报告页面查看细节")
        except Exception as e:
            Executor.log.exception(f"执行测试计划: 【{plan.name}】失败: {str(e)}")
            Executor.log.error(f"执行测试计划: 【{plan.name}】失败: {str(e)}")

    @staticmethod
    async def run_multiple(executor: int, env: int, case_list: List[int], mode=0, plan_id: int = None, ordered=False,
                           report_dict: dict = None, retry_minutes: int = 0):
        try:
            current_env = await EnvironmentDao.query_env(env)
            if executor != 0:
                # 说明不是系统执行
                user = await UserDao.query_user(executor)
                name = user.name if user is not None else "未知"
            else:
                name = "pity机器人"
            st = time.perf_counter()
            # step1: 新增测试报告数据
            report_id = await TestReportDao.start(executor, env, mode, plan_id=plan_id)
            # step2: 开始执行用例
            result_data = defaultdict(list)
            # step3: 将报告改为 running状态
            await TestReportDao.update(report_id, 1)
            # step4: 执行用例并搜集数据
            if not ordered:
                await asyncio.gather(
                    *(Executor.run_single(env, result_data, report_id, c, retry_minutes=retry_minutes) for c in
                      case_list))
            else:
                # 顺序执行
                for c in case_list:
                    await Executor.run_single(env, result_data, report_id, c, retry_minutes=retry_minutes)
            ok, fail, skip, error = 0, 0, 0, 0
            for case_id, status in result_data.items():
                for s in status:
                    if s == 0:
                        ok += 1
                    elif s == 1:
                        fail += 1
                    elif s == 2:
                        error += 1
                    else:
                        skip += 1
            cost = time.perf_counter() - st
            cost = "%.2f" % cost
            # step5: 回写数据到报告
            report = await TestReportDao.end(report_id, ok, fail, error, skip, 3, cost)
            if report_dict is not None:
                report_dict[env] = {
                    "report_url": f"{Config.SERVER_REPORT}{report_id}",
                    "start_time": report.start_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "end_time": report.finished_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "success": ok,
                    "failed": fail,
                    "total": ok + fail + error + skip,
                    "error": error,
                    "skip": skip,
                    "executor": name,
                    "cost": cost,
                    "plan_result": "通过" if ok + fail + error + skip > 0 and fail + error == 0 else '未通过',
                    "env": current_env.name,
                }
            return report_id
        except Exception as e:
            raise Exception(f"批量执行用例失败: {e}")


if __name__ == "__main__":
    a = Executor()
    temp = json.dumps({"a": {"b": [{"c": 1, "d": 2}]}})
    ans = a.parse_variable(temp, "${a.b.#name.c}", {"name": 0})
    print(ans)
