import json

from app.dao.test_case.TestCaseDao import TestCaseDao
from app.middleware.HttpClient import Request
from app.utils.logger import Log


class Executor(object):
    log = Log("executor")

    @staticmethod
    def run(case_id: int):
        result = dict()
        try:
            case_info, err = TestCaseDao.query_test_case(case_id)
            if err:
                return result, err
            # 说明取到了用例数据
            if case_info.request_header != "":
                headers = json.loads(case_info.request_header)
            else:
                headers = dict()
            if case_info.body != '':
                body = case_info.body
            else:
                body = None
            request_obj = Request(case_info.url, headers=headers, data=body)
            method = case_info.request_method.upper()
            response_info = request_obj.request(method)
            return response_info, None
        except Exception as e:
            Executor.log.error(f"执行用例失败: {str(e)}")
            return result, f"执行用例失败: {str(e)}"
