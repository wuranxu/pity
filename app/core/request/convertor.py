__author__ = "woody"

from typing import List

from app.schema.request import RequestInfo

"""
request转换器，支持har到
"""


class Convertor(object):

    @staticmethod
    def convert(file, regex: str = None) -> List[RequestInfo]:
        raise NotImplementedError
