import json
import time

import aiohttp


class AsyncRequest(object):

    def __init__(self, url: str, timeout=15, **kwargs):
        self.url = url
        self.kwargs = kwargs
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    def get_cookie(self, session):
        cookies = session.cookie_jar.filter_cookies(self.url)
        return {k: v.value for k, v in cookies.items()}

    async def invoke(self, method: str):
        start = time.time()
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
            async with session.request(method, self.url, timeout=self.timeout, **self.kwargs) as resp:
                if resp.status != 200:
                    return await self.collect(False, self.kwargs.get("data"), resp.status)
                cost = "%.0fms" % ((time.time() - start) * 1000)
                response = await AsyncRequest.get_resp(resp)
                cookie = self.get_cookie(session)
                return await self.collect(True, self.kwargs.get("data"), resp.status, response,
                                          resp.headers, resp.request_info.headers, elapsed=cost,
                                          cookies=cookie
                                          )

    @staticmethod
    async def get_resp(resp):
        try:
            data = await resp.json(encoding='utf-8')
        except:
            data = await resp.text()
        return data

    @staticmethod
    async def collect(status, request_data, status_code=200, response=None, response_header=None,
                      request_header=None, cookies=None, elapsed=None, msg="success"):
        """
        收集http返回数据
        :param status: 请求状态
        :param request_data: 请求入参
        :param status_code: 状态码
        :param response: 相应
        :param response_header: 返回header
        :param request_header:  请求header
        :param cookies:  cookie
        :param elapsed: 耗时
        :param msg: 报错信息
        :return:
        """
        request_header = {k: v for k, v in request_header.items()} if request_header is not None else {}
        response_header = {k: v for k, v in response_header.items()} if response_header is not None else {}
        cookies = {k: v for k, v in cookies.items()} if cookies is not None else {}
        return {
            "status": status, "response": response, "status_code": status_code,
            "request_data": request_data if isinstance(request_data, str) or request_data is None else json.dumps(
                request_data,
                ensure_ascii=False),
            "response_header": response_header, "request_header": request_header,
            "msg": msg, "elapsed": elapsed, "cookies": cookies,
        }
