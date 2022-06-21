"""
流量录制->生成case功能
record steps and generate testcase
"""
import asyncio
import json
import re

from app.core.ws_connection_manager import ws_manage
from app.enums.MessageEnum import WebSocketMessageEnum
from app.middleware.RedisManager import RedisHelper
from app.schema.request import RequestInfo


class PityRecorder(object):
    def request(self, flow):
        flow.request.headers["X-Forwarded-For"] = flow.client_conn.address[0]

    async def response(self, flow):
        addr = flow.client_conn.address[0]
        flow.response.headers["X-Forwarded-For"] = addr
        record = await RedisHelper.get_address_record(addr)
        if not record:
            return
        data = json.loads(record)
        pattern = re.compile(data.get("regex"))
        if re.findall(pattern, flow.request.url):
            # 忽略js、css等文件
            if flow.request.method.lower() == "options":
                return
            if flow.request.url.endswith(("js", "css", "ttf", "jpg", "svg", "gif")):
                return
            # 说明已开启录制开关，记录状态
            request_data = RequestInfo(flow)
            dump_data = request_data.dumps()
            await RedisHelper.cache_record(addr, dump_data)
            asyncio.create_task(ws_manage.send_data(data.get("user_id"), WebSocketMessageEnum.RECORD,
                                                    dump_data))
