import json

from app.core.constructor.constructor import ConstructorAbstract
from app.crud.config.DbConfigDao import DbConfigDao
from app.models.constructor import Constructor


class SqlConstructor(ConstructorAbstract):

    @staticmethod
    async def run(executor, env, index, path, params, req_params, constructor: Constructor, **kwargs):
        try:
            executor.append(f"当前路径: {path}, 第{index + 1}条{ConstructorAbstract.get_name(constructor)}")
            data = json.loads(constructor.constructor_json)
            database = data.get("database")
            sql = data.get("sql")
            executor.append(f"当前{ConstructorAbstract.get_name(constructor)}类型为sql, 数据库名: {database}\nsql: {sql}\n")
            sql_data = await DbConfigDao.execute_sql(env, database, sql)
            params[constructor.value] = sql_data
            executor.append(
                f"当前{ConstructorAbstract.get_name(constructor)}返回变量: {constructor.value}\n返回值:\n {sql_data}\n")
        except Exception as e:
            raise Exception(
                f"{path}->{constructor.name} 第{index + 1}个{ConstructorAbstract.get_name(constructor)}执行失败: {e}")
