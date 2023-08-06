from pydantic import BaseModel, Field
from typing import List


class SwitchOnOff(BaseModel):
    msg: str
    tracking_ids: List[str] = Field(alias='trackingIDs')


class SwitchOnOffResponse(BaseModel):
    data: SwitchOnOff
    status: int
