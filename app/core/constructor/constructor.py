from abc import ABC

from app.models.constructor import Constructor


class ConstructorAbstract(ABC):

    @staticmethod
    def run(executor, env, index, path, params, req_params, constructor: Constructor, **kwargs):
        pass

    @staticmethod
    def get_name(constructor):
        return '前置条件' if not constructor.suffix else '后置条件'
