from typing import List

from pydantic import BaseModel


class NotificationForm(BaseModel):
    personal: List[int] = None
    broadcast: List[int] = None
