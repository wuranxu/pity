from typing import List

from pydantic import BaseModel, validator

from app.models.schema.base import PityModel


class PityTestPlanForm(BaseModel):
    id: int = None
    project_id: int
    name: str
    priority: str
    env: List[int]
    cron: str
    ordered: bool
    case_list: List[int]
    pass_rate: int
    receiver: List[int]
    msg_type: List[int]
    retry_minutes: int

    @validator("case_list", "project_id", "env", "cron", "ordered", "priority", "name", "pass_rate", "receiver")
    def name_not_empty(cls, v):
        return PityModel.not_empty(v)
