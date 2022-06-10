import json
import re
from typing import List

from app.core.request.convertor import Convertor
from app.core.request.request import RequestInfo
from app.excpetions.convert.ConvertException import HarConvertException


class HarConvertor(Convertor):
    @staticmethod
    def convert(file, regex: str = None) -> List[RequestInfo]:
        try:
            with open(file, "r", encoding="utf-8") as f:
                ans = []
                flag = None
                if regex is not None:
                    flag = re.compile(regex)
                # 加载har请求数据
                data = json.load(f)
                entries = data.get("log", {}).get("entries")
                if not entries:
                    raise HarConvertException("entries数据为空")
                for entry in entries:
                    # 如果是fetch或xhr接口，说明是http请求（暂不支持js)
                    if entry.get("_resourceType").lower() in ("fetch", "xhr"):
                        info = RequestInfo()
                        request_data = entry.get("request")
                        info.url = request_data.get("url")
                        if flag is not None and not re.findall(flag, info.url):
                            # 由于不符合预期的url，所以过滤掉
                            continue
                        response_data = entry.get("response")
                        info.body = HarConvertor.get_body(request_data)
                        info.status_code = response_data.get("status")
                        info.request_method = request_data.get("method")
                        info.request_headers = HarConvertor.get_kv(request_data)
                        info.response_headers = HarConvertor.get_kv(response_data)
                        info.cookies = HarConvertor.get_kv(response_data, "cookies")
                        info.request_cookies = HarConvertor.get_kv(request_data, "cookies")
                        info.response_content = response_data.get("content", {}).get("text")
                        ans.append(info)
                return ans
        except HarConvertException as e:
            raise HarConvertException(f"har文件转换异常: {e}")
        except Exception as e:
            raise HarConvertException(f"har文件转换失败: {e}")

    @staticmethod
    def get_kv(request_data: dict, key: str = "headers") -> dict:
        """
        通过response/request获取header信息
        :param key:
        :param request_data:
        :return:
        """
        headers = request_data.get(key)
        result = dict()
        for h in headers:
            result[h.get("name")] = h.get("value")
        return result

    @staticmethod
    def get_body(request_data: dict):
        data = request_data.get("postData", {})
        return data.get("text")


if __name__ == "__main__":
    requests = HarConvertor.convert("./pity.fun.har", "juejin.cn")
    print(requests)
