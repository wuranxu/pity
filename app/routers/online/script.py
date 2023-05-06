from fastapi import Depends

from app.handler.fatcory import PityResponse
from app.routers import Permission
from app.routers.online.sql import router
from app.schema.script import PyScriptForm

tag = "Python脚本"


@router.post("/script")
def execute_py_script(data: PyScriptForm, _=Depends(Permission())):
    try:
        loc = dict()
        exec(data.command, loc)
        value = loc.get(data.value)
        return PityResponse.success(data=value)
    except Exception as err:
        return PityResponse.failed(err)
