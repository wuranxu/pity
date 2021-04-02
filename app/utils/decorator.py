from functools import wraps

from flask import request, jsonify

from app import pity
from app.middleware.Jwt import UserToken

FORBIDDEN = "对不起, 你没有足够的权限"


class SingletonDecorator:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


def permission(role=pity.config.get("GUEST")):
    def login_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                headers = request.headers
                token = headers.get('token')
                if token is None:
                    return jsonify(dict(code=401, msg="用户信息认证失败, 请检查"))
                user_info = UserToken.parse_token(token)
                # 这里把user信息写入kwargs
                kwargs["user_info"] = user_info
            except Exception as e:
                return jsonify(dict(code=401, msg=str(e)))
            # 判断用户权限是否足够, 如果不足够则直接返回，不继续
            if user_info.get("role", 0) < role:
                return jsonify(dict(code=400, msg=FORBIDDEN))
            return func(*args, **kwargs)

        return wrapper

    return login_required
