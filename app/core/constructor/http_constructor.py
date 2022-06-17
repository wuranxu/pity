import json

from app.core.constructor.constructor import ConstructorAbstract
from app.crud.config.AddressDao import PityGatewayDao
from app.middleware.AsyncHttpClient import AsyncRequest
from app.models.constructor import Constructor


class HttpConstructor(ConstructorAbstract):

    @staticmethod
    async def run(executor, env, index, path, params, req_params, constructor: Constructor, **kwargs):
        try:
            executor.append(f"当前路径: {path}, 第{index + 1}条{HttpConstructor.get_name(constructor)}")
            data = json.loads(constructor.constructor_json)
            url = data.get("url")
            if data.get("base_path"):
                base_path = await PityGatewayDao.query_gateway(env, data.get("base_path"))
                url = f"{base_path}{url}"
            headers = data.get("headers")
            if isinstance(headers, str):
                headers = json.loads(data.get("headers"))
            client = await AsyncRequest.client(url=url, body_type=data.get("body_type"), headers=headers,
                                               body=data.get("body"))
            resp = await client.invoke(data.get("request_method"))
            executor.append(f"当前{ConstructorAbstract.get_name(constructor)}类型为http, url: {url}")
            if constructor.value:
                params[constructor.value] = resp
            executor.append(
                f"当前{ConstructorAbstract.get_name(constructor)}返回变量: {constructor.value}\n返回值:\n {resp}\n")
        except Exception as e:
            raise Exception(
                f"{path}->{constructor.name} 第{index + 1}个{HttpConstructor.get_name(constructor)}执行失败: {e}")
