import json

from app.core.constructor.constructor import ConstructorAbstract
from app.crud.config.RedisConfigDao import PityRedisConfigDao
from app.models.constructor import Constructor


class RedisConstructor(ConstructorAbstract):

    @staticmethod
    async def run(executor, env, index, path, params, constructor: Constructor, **kwargs):
        try:
            executor.append(f"当前路径: {path}, 第{index + 1}条{ConstructorAbstract.get_name(constructor)}")
            data = json.loads(constructor.constructor_json)
            redis = data.get("redis")
            command = data.get("command")
            executor.append(f"当前{ConstructorAbstract.get_name(constructor)}类型为redis, 名称: {redis}\n命令: {command}\n")
            command_result = await PityRedisConfigDao.execute_command(command=command, name=redis, env=env)
            executor.append(
                f"当前{ConstructorAbstract.get_name(constructor)}返回变量: {constructor.value}\n返回值:\n {command_result}\n")
            return command_result
        except Exception as e:
            raise Exception(
                f"{path}->{constructor.name} 第{index + 1}个{ConstructorAbstract.get_name(constructor)}执行失败: {e}")
