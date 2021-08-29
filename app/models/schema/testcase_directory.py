from pydantic import BaseModel, validator

from app.models.schema.base import PityModel


class PityTestcaseDirectoryForm(BaseModel):
    id: int = None
    name: str
    project_id: int
    parent: int = None

    @validator("name", "project_id")
    def name_not_empty(cls, v):
        return PityModel.not_empty(v)
