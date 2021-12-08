import json

from app.core.constructor.constructor import ConstructorAbstract
from app.models.constructor import Constructor


class PythonConstructor(ConstructorAbstract):

    @staticmethod
    async def run(executor, env, index, path, params, req_params, constructor: Constructor, **kwargs):
        try:
            executor.append(f"当前路径: {path}, 第{index + 1}条构造方法")
            script = json.loads(constructor.constructor_json)
            command = script['command']
            executor.append(f"当前构造方法类型为python脚本\n{command}")
            loc = dict()
            exec(command, loc)
            py_data = loc[constructor.value]
            if not isinstance(py_data, str):
                py_data = json.dumps(params[constructor.value], ensure_ascii=False)
            executor.append(f"当前构造方法返回变量: {constructor.value}\n返回值:\n {py_data}\n")
        except Exception as e:
            raise Exception(f"{path}->{constructor.name} 第{index + 1}个构造方法执行失败: {e}")
