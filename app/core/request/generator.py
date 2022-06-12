__author__ = "woody"

import json
from collections import defaultdict
from json import JSONDecodeError
from typing import List

from loguru import logger

from app.core.request.request import RequestInfo
from app.excpetions.convert.GenerateException import GenerateException
from app.models.test_case import TestCase

"""
case生成器，根据RequestInfo数组生成
"""


class CaseGenerator(object):
    # 忽略的字段
    ignored = (
        "Content-Type", "Connection", "Date", "Content-Length", "Host", "access-control-allow-credentials",
        "access-control-allow-origin", "User-Agent", "Server"
    )

    @staticmethod
    def ignore(key: str):
        for ig in CaseGenerator.ignored:
            if key.lower().endswith(ig.lower()):
                return True
        return False

    @staticmethod
    def generate_case(requests: List[RequestInfo]) -> List[TestCase]:
        pass

    @staticmethod
    def extract_field(requests: List[RequestInfo]) -> List[str]:
        """
        遍历接口，并提取其中的变量
        :param requests:
        :return:
        """
        var_pool = defaultdict(list)
        replaced = []
        for i in range(len(requests)):
            # 记录变量
            CaseGenerator.record_vars(requests[i], var_pool, f"http_res_{i + 1}")
            if i > 0:
                CaseGenerator.replace_vars(requests[i], var_pool, replaced)
        return replaced

    @staticmethod
    def replace_vars(request: RequestInfo, ans: dict, replaced: list):
        CaseGenerator.replace_url(request, ans, replaced)
        CaseGenerator.replace_headers(request, ans, replaced)
        CaseGenerator.replace_body(request, ans, replaced)

    @staticmethod
    def record_vars(request: RequestInfo, ans: dict, var_name: str):
        CaseGenerator.split_headers(request, ans, f"{var_name}.response_headers")
        CaseGenerator.split_body(request, ans, f"{var_name}.response")

    @staticmethod
    def dfs(body, path: str, ans: dict, headers: bool = False):
        if isinstance(body, list):
            for i in range(len(body)):
                c_path = f"{path}.{i}"
                CaseGenerator.dfs(body[i], c_path, ans, headers)
        elif isinstance(body, dict):
            for k, v in body.items():
                c_path = f"{path}.{k}"
                CaseGenerator.dfs(v, c_path, ans, headers)
        else:
            if not headers or not CaseGenerator.ignore(path):
                # 如果是bool值，需要特殊处理一下，因为Python get False/True会变成get 0 1
                if body is not None:
                    if isinstance(body, bool):
                        ans[str(body)].append(path)
                    else:
                        ans[body].append(path)

    @staticmethod
    def split_body(request: RequestInfo, ans: dict, var_name: str = ''):
        if request.body:
            try:
                body = json.loads(request.response_content)
                CaseGenerator.dfs(body, var_name, ans)
            except JSONDecodeError:
                # 可能body不是JSON，跳过
                pass
            except Exception as e:
                raise GenerateException(f"解析接口body变量出错: {e}")

    @staticmethod
    def split_headers(request: RequestInfo, ans: dict, var_name: str = ""):
        try:
            CaseGenerator.dfs(request.response_headers, var_name, ans, True)
        except Exception as e:
            raise GenerateException(f"解析接口headers变量出错: {e}")

    @staticmethod
    def replace_headers(request: RequestInfo, ans: dict, replaced: list):
        for k, v in request.request_headers.items():
            if ans.get(v):
                request.request_headers[k] = "${%s}" % ans.get(v)[0]
                replaced.append("%s => ${%s}" % (k, ans.get(v)[0]))

    @staticmethod
    def replace_body(request: RequestInfo, ans: dict, replaced: list):
        if request.body:
            try:
                data = json.loads(request.body)
                var_type = list()
                CaseGenerator.dfs_replace(data, ans, var_type, replaced)
                result = json.dumps(data, ensure_ascii=False)
                for v in var_type:
                    result = result.replace(f'"{v}"', f"{v}")
                request.body = result
            except JSONDecodeError:
                pass
            except Exception as e:
                logger.error(f"转换body变量失败: {e}")

    @staticmethod
    def dfs_replace(body, ans: dict, var_type: list, replaced: list):
        if isinstance(body, dict):
            for k, v in body.items():
                string, value = CaseGenerator.dfs_replace(v, ans, var_type, replaced)
                if value is not None:
                    body[k] = "${%s}" % value
                    if not string:
                        var_type.append("${%s}" % value)
        elif isinstance(body, list):
            for i in range(len(body)):
                string, value = CaseGenerator.dfs_replace(body[i], ans, var_type, replaced)
                if value is not None:
                    body[i] = "${%s}" % value
                    if not string:
                        var_type.append("${%s}" % value)
        else:
            body_str = body
            if isinstance(body, bool):
                body_str = str(body)
            if ans.get(body_str):
                replaced.append("%s => ${%s}" % (body_str, ans.get(body_str)[0]))
                if not isinstance(body_str, str):
                    return False, ans.get(body_str)[0]
                return True, ans.get(body_str)[0]
            return None, None

    @staticmethod
    def replace_url(request: RequestInfo, ans: dict, replaced: list):
        """
        拆解url，将url里面的路由path和query参数
        :return:
        """
        # 获取前缀和后缀
        url_query = request.url.split("?")
        if len(url_query) == 1:
            query_list = list()
            prefix = url_query[0]
        else:
            prefix, suffix = url_query
            query_list = suffix.split("&")
        http, prefix = prefix.split("//")
        url_list = prefix.split("/")
        new_url = []
        new_query = []
        for u in url_list:
            if ans.get(u):
                new_url.append(ans.get(u)[0])
                replaced.append("%s => ${%s}" % (u, ans.get(u)[0]))
            else:
                new_url.append(u)
        for q in query_list:
            k, v = q.split("=")
            if ans.get(v):
                new_query.append("%s=${%s}" % (k, ans.get(v)[0]))
                replaced.append("%s => ${%s}" % (k, ans.get(v)[0]))
            else:
                new_query.append(q)
        if len(query_list) == 0:
            request.url = f"{http}//{'/'.join(new_url)}"
            return
        request.url = f"{http}//{'/'.join(new_url)}?{'&'.join(new_query)}"

# if __name__ == "__main__":
#     req = HarConvertor.convert("./pity.fun.har", "api.pity.fun")
#     for r in req:
#         print(r)
#     CaseGenerator.extract_field(req)
#     for r in req:
#         print(r)
