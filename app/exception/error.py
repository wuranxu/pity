class AuthError(Exception):
    """user authorization error
    """


class CaseParametersError(Exception):
    """extract parameters error
    """


class ParamsError(ValueError):
    """request params error
    """


class RedisError(Exception):
    """redis error
    """


class RpcError(Exception):
    """rpc error
    """
