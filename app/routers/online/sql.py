from fastapi import APIRouter, Depends

from app.dao.config.DbConfigDao import DbConfigDao
from app.handler.fatcory import PityResponse
from app.models.schema.online_sql import OnlineSQLForm
from app.routers import Permission

router = APIRouter(prefix="/online")


@router.post("/sql")
async def execute_sql(data: OnlineSQLForm, user_info=Depends(Permission())):
    try:
        result = await DbConfigDao.online_sql(data.id, data.sql)
        columns, result = PityResponse.parse_sql_result(result)
        return PityResponse.success(data=dict(result=result, columns=columns))
    except Exception as err:
        return PityResponse.failed(err)


@router.get("/tables")
async def list_tables(user_info=Depends(Permission())):
    try:
        result, table_map = await DbConfigDao.query_database_and_tables()
        return PityResponse.success(dict(database=result, tables=table_map))
    except Exception as err:
        return PityResponse.failed(err)
