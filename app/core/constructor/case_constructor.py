import json

from app.core.constructor.constructor import ConstructorAbstract
from app.crud.test_case.TestCaseDao import TestCaseDao
from app.models.constructor import Constructor


class TestcaseConstructor(ConstructorAbstract):

    @staticmethod
    async def run(executor, env, index, path, params, req_params, constructor: Constructor, **kwargs):
        try:
            data = json.loads(constructor.constructor_json)
            case_id = data.get("constructor_case_id")
            if not case_id:
                raise Exception("未获取到前/后置条件的用例id, 请检查前置条件")
            testcase, err = await TestCaseDao.async_query_test_case(case_id)
            if err:
                raise Exception(f"用例: [{case_id}]不存在:")
            executor.append(f"当前路径: {path}, 第{index + 1}条{ConstructorAbstract.get_name(constructor)}")
            # 说明是case
            executor_class = kwargs.get('executor_class')(executor.logger)
            new_param = data.get("params")
            if new_param:
                temp = json.loads(new_param)
                req_params.update(temp)
            result, err = await executor_class.run(env, case_id, params, req_params, f"{path}->{testcase.name}")
            if err:
                raise Exception(err)
            if not result["status"]:
                raise Exception(f"断言失败, 断言数据: {result.get('asserts', 'unknown')}")
            params[constructor.value] = result
        except Exception as e:
            raise Exception(
                f"{path}->{constructor.name} 第{index + 1}个{ConstructorAbstract.get_name(constructor)}执行失败: {e}")
