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
    url: str
    body: str
    request_method: str
    # request_data: str
    request_headers: dict
    response_headers: dict
    cookies: dict
    request_cookies: dict
    response_content: str
    status_code: int

    def __init__(self, flow=None, **kwargs):
        if flow:
            kwargs.update(
                dict(status_code=flow.response.status_code,
                     url=flow.request.url,
                     request_method=flow.request.method,
                     request_headers=dict(flow.request.headers),
                     response_headers=dict(flow.response.headers),
                     response_content=self.get_response(flow.response),
                     body=self.get_body(flow.request),
                     cookies=dict(flow.response.cookies),
                     request_cookies=dict(flow.request.cookies),
                     ))
        super().__init__(**kwargs)

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
            return ''
        content_type = request.headers.get("Content-Type")
        if "json" in content_type.lower():
            return cls.translate_json(request.text)
        if "text" in content_type.lower() or "xml" in content_type.lower():
            return request.text
        return request.data.decode('utf-8')

    def dumps(self):
        return json.dumps(self.dict(), ensure_ascii=False)
