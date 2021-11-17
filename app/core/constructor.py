from abc import ABC

from app.models.constructor import Constructor


class ConstructorAbstract(ABC):

    @staticmethod
    def run(executor, env, index, path, params, req_params, constructor: Constructor, **kwargs):
        pass
