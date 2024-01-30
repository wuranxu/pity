from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import desc

from app.crud.operation.PityOperationDao import PityOperationDao
from app.handler.fatcory import PityResponse
from app.models.operation_log import PityOperationLog
from app.routers import Permission

router = APIRouter(prefix="/operation")


# 获取用户操作记录
@router.get("/list")
async def list_user_operation(start_time: str, end_time: str, user_id: int, tag: str = None, _=Depends(Permission())):
    try:
        start = datetime.strptime(start_time, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
        end = datetime.strptime(end_time, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=0)
        records = await PityOperationDao.select_list(user_id=user_id, tag=tag, condition=[
            PityOperationLog.operate_time.between(start, end)], _sort=[desc(PityOperationLog.operate_time)])
        return PityResponse.records(records)
    except Exception as e:
        return PityResponse.failed(e)


# 获取用户操作记录热力图以及参与的项目数量
@router.get("/count")
async def list_user_activities(user_id: int, start_time: str, end_time: str, _=Depends(Permission())):
    try:
        start = datetime.strptime(start_time, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
        end = datetime.strptime(end_time, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=0)
        records = await PityOperationDao.count_user_activities(user_id, start, end)
        ans = list()
        date_index = dict()
        for r in records:
            # 解包日期和数量
            date, count = r
            date_str = date.strftime("%Y-%m-%d")
            if date_index.get(date_str) is None:
                ans.append(dict(date=date_str, count=count))
                date_index[date_str] = len(ans) - 1
            else:
                ans[date_index[date_str]]['count'] += 1
        return PityResponse.success(ans)
    except Exception as e:
        return PityResponse.failed(e)
