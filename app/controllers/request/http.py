from flask import Blueprint
from flask import jsonify
from flask import request

from app import pity
from app.middleware.HttpClient import Request
from app.utils.decorator import permission

req = Blueprint("request", __name__, url_prefix="/request")


@req.route("/http", methods=['POST'])
@permission(pity.config.get("ADMIN"))
def http_request(user_info):
    data = request.get_json()
    method = data.get("method")
    if not method:
        return jsonify(dict(code=101, msg="请求方式不能为空"))
    url = data.get("url")
    if not url:
        return jsonify(dict(code=101, msg="请求地址不能为空"))
    body = data.get("body")
    headers = data.get("headers")
    r = Request(url, data=body, headers=headers)
    response = r.request(method)
    if response.get("status"):
        return jsonify(dict(code=0, data=response, msg="操作成功"))
    return jsonify(dict(code=110, data=response, msg=response.get("msg")))
