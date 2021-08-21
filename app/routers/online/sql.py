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
        return PityResponse.success(data=result)
    except Exception as err:
        return PityResponse.failed(err)


@router.get("/tables")
async def list_tables(user_info=Depends(Permission())):
    try:
        result = await DbConfigDao.query_database_and_tables()
        return PityResponse.success(result)
    except Exception as err:
        return PityResponse.failed(err)
