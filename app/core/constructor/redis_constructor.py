import json

from app.core.constructor.constructor import ConstructorAbstract
from app.dao.config.RedisConfigDao import PityRedisConfigDao
from app.models.constructor import Constructor


class RedisConstructor(ConstructorAbstract):

    @staticmethod
    async def run(executor, env, index, path, params, req_params, constructor: Constructor, **kwargs):
        try:
            executor.append(f"当前路径: {path}, 第{index + 1}条构造方法")
            data = json.loads(constructor.constructor_json)
            redis = data.get("redis")
            command = data.get("command")
            executor.append(f"当前构造方法类型为redis, 名称: {redis}\n命令: {command}\n")
            command_result = await PityRedisConfigDao.execute_command(command=command, name=redis, env=env)
            params[constructor.value] = command_result
            executor.append(f"当前构造方法返回变量: {constructor.value}\n返回值:\n {command_result}\n")
        except Exception as e:
            raise Exception(f"{path}->{constructor.name} 第{index + 1}个构造方法执行失败: {e}")
