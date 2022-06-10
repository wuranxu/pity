__author__ = "woody"

import json
from typing import TypeVar

import pydantic
from loguru import logger

"""
translate mitmproxy request and response data
"""

body = TypeVar("body", bytes, str)


class RequestInfo(pydantic.BaseModel):
    url: str = None
    body: body = None
    request_method: str = None
    request_data: str = None
    request_headers: dict = None
    response_headers: dict = None
    cookies: dict = None
    request_cookies: dict = None
    response_content: str = None
    status_code: int = None

    def __init__(self, flow=None):
        super().__init__()
        if flow:
            self.status_code = flow.response.status_code
            self.url = flow.request.url
            self.request_method = flow.request.method
            self.request_headers = dict(flow.request.headers)
            self.response_headers = dict(flow.response.headers)
            self.response_content = self.get_response(flow.response)
            self.body = self.get_body(flow.request)
            self.cookies = dict(flow.response.cookies)
            self.request_cookies = dict(flow.request.cookies)

    def from_dict(self, **kwargs):
        for k, v in kwargs:
            if not hasattr(self, k):
                raise Exception(f"set RequestInfo error, no field: {k}")
            setattr(self, k, v)

    @classmethod
    def translate_json(cls, text):
        try:
            return json.dumps(json.loads(text), indent=4, ensure_ascii=False)
        except Exception as e:
            logger.bind(name=None).warning(f"解析json格式请求失败: {e}")
            return text

    @classmethod
    def get_response(cls, response):
        content_type = response.headers.get("Content-Type")
        if "json" in content_type.lower():
            return cls.translate_json(response.text)
        if "text" in content_type.lower() or "xml" in content_type.lower():
            return response.text
        return response.data.decode('utf-8')

    @classmethod
    def get_body(cls, request):
        if len(request.content) == 0:
            return None
        content_type = request.headers.get("Content-Type")
        if "json" in content_type.lower():
            return cls.translate_json(request.text)
        if "text" in content_type.lower() or "xml" in content_type.lower():
            return request.text
        return request.data.decode('utf-8')

    def dumps(self):
        return json.dumps(self.dict(), ensure_ascii=False)
