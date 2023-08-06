from pydantic import BaseModel, Field
from typing import List


class CommandData(BaseModel):
    msg: str
    tracking_ids: List[str] = Field(alias='trackingIDs')


class CommandResponse(BaseModel):
    data: CommandData
    status: int
