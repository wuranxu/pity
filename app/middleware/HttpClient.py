import datetime

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
                response = self.client.get(self.url, **self.kwargs)
            elif method.upper() == 'POST':
                response = self.client.post(self.url, **self.kwargs)
            else:
                response = self.client.request(method, self.url, **self.kwargs)
            status_code = response.status_code
            if status_code != 200:
                return Request.response(False, status_code)
            elapsed = Request.get_elapsed(response.elapsed)
            data = response.json()
            return Request.response(True, 200, data, response.headers, response.request.headers, elapsed=elapsed)
        except Exception as e:
            return Request.response(False, status_code, msg=str(e), elapsed=elapsed)

    def post(self):
        return self.request("POST")

    @staticmethod
    def response(status, status_code=200, response=None, response_header=None,
                 request_header=None, elapsed=None, msg="success"):
        request_header = {k: v for k, v in request_header.items()}
        response_header = {k: v for k, v in response_header.items()}
        return {
            "status": status, "response": response, "status_code": status_code,
            "response_header": response_header, "request_header": request_header,
            "msg": msg, "elapsed": elapsed,
        }
