from flask import Blueprint

from app.handler.page import PageHandler
from app.utils.decorator import permission

pr = Blueprint("project", __name__, url_prefix="/project")


@pr.route("/list")
@permission()
def list_project(user_info):
    """
    获取项目列表
    :param user_info:
    :return:
    """
    page, size = PageHandler.page()
    user_role = user_info["role"]
