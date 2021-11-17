from pydantic import BaseModel, validator

from app.models.schema.base import PityModel


class WechatForm(BaseModel):
    signature: str
    timestamp: int
    nonce: str
    echostr: str
