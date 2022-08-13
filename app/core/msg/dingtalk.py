import os
from urllib.parse import quote

from app.core.msg.notification import Notification
from app.middleware.AsyncHttpClient import AsyncRequest
from config import Config


class DingTalk(Notification):
    dingtalk_md = os.path.join(Config.MARKDOWN_PATH, "test_report.md")

    def __init__(self, openapi: str):
        """
        钉钉通知openurl
        :param openapi:
        """
        self.openapi = openapi

    @staticmethod
    def render_markdown(**testdata):
        with open(DingTalk.dingtalk_md, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
            return markdown_text.format(**testdata)

    async def send_msg(self, subject, content, attachment=None, *receiver, **kwargs):
        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": subject,
                "text": "![screenshot](https://static.pity.fun/picture/走势监测.png)\n%s" % content,
                "singleTitle": '👉 查看报告',
                "singleURL": f"""dingtalk://dingtalkclient/page/link?url={quote(kwargs.get("link"))}&pc_slide=false"""
            },
            "at": {
                "atMobiles": receiver,
            }
        }
        # data = {
        #     "msgtype": "markdown",
        #     "markdown": {
        #         "title": subject,
        #         "text": content,
        #     },
        #     "at": {
        #         "atMobiles": receiver,
        #     }
        # }
        r = AsyncRequest(self.openapi, headers={'Content-Type': 'application/json'}, timeout=15, json=data)
        response = await r.invoke("POST")
        if not response.get("status"):
            raise Exception("发送钉钉通知失败")
