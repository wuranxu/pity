import hashlib
from datetime import timedelta, datetime

import jwt
from jwt.exceptions import ExpiredSignatureError

EXPIRED_HOUR = 72


class UserToken(object):
    key = 'pityToken'
    salt = 'pity'

    @staticmethod
    def get_token(data):
        expire = datetime.now() + timedelta(hours=EXPIRED_HOUR)
        new_data = dict({"exp": datetime.utcnow() + timedelta(hours=EXPIRED_HOUR)}, **data)
        return expire.timestamp(), jwt.encode(new_data, key=UserToken.key)

    @staticmethod
    def parse_token(token):
        try:
            return jwt.decode(token, key=UserToken.key, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise Exception("登录状态已过期, 请重新登录")
        except Exception:
            raise Exception("登录状态校验失败, 请重新登录")

    @staticmethod
    def add_salt(password):
        m = hashlib.md5()
        bt = f"{password}{UserToken.salt}".encode("utf-8")
        m.update(bt)
        return m.hexdigest()
