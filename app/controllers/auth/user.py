from flask import Blueprint
from flask import jsonify

auth = Blueprint("auth", __name__, url_prefix="/auth")


# 这里以auth.route注册的函数都会自带/auth，所以url是/auth/register
@auth.route("/register")
def register():
    return jsonify(dict(status=True, msg="注册成功"))
