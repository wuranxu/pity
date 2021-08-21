import datetime
import json

import requests


class Request(object):

    def __init__(self, url, session=False, **kwargs):
        self.url = url
        self.session = session
        self.kwargs = kwargs
        if self.session:
            self.client = requests.session()
            return
        self.client = requests

    def get(self):
        return self.request("GET")

    @staticmethod
    def get_elapsed(timer: datetime.timedelta):
        if timer.seconds > 0:
            return f"{timer.seconds}.{timer.microseconds // 1000}s"
        return f"{timer.microseconds // 100}ms"

    def request(self, method: str):
        status_code = 0
        elapsed = "-1ms"
        try:
            if method.upper() == "GET":
                response = self.client.get(self.url, **self.kwargs, timeout=30)
            elif method.upper() == 'POST':
                response = self.client.post(self.url, **self.kwargs, timeout=30)
            else:
                response = self.client.request(method, self.url, **self.kwargs, timeout=30)
            status_code = response.status_code
            if status_code != 200:
                return Request.response(False, self.kwargs.get("data"), status_code)
            elapsed = Request.get_elapsed(response.elapsed)
            data = self.get_response(response)
            return Request.response(True, self.kwargs.get("data"), 200, data, response.headers,
                                    response.request.headers, elapsed=elapsed,
                                    cookies=response.cookies)
        except Exception as e:
            return Request.response(False, self.kwargs.get("data"), status_code, msg=str(e), elapsed=elapsed)

    def post(self):
        return self.request("POST")

    def get_response(self, response):
        try:
            return response.json()
        except:
            return response.text

    @staticmethod
    def response(status, request_data, status_code=200, response=None, response_headers=None,
                 request_headers=None, cookies=None, elapsed=None, msg="success"):
        request_headers = {k: v for k, v in request_headers.items()} if request_headers is not None else {}
        response_headers = {k: v for k, v in response_headers.items()} if response_headers is not None else {}
        cookies = {k: v for k, v in cookies.items()} if cookies is not None else {}
        return {
            "status": status, "response": response, "status_code": status_code,
            "request_data": request_data if isinstance(request_data, str) else json.dumps(request_data,
                                                                                          ensure_ascii=False),
            "response_headers": response_headers, "request_headers": request_headers,
            "msg": msg, "cost": elapsed, "cookies": cookies,
        }
