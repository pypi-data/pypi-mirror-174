from pydantic import BaseModel, Field
from typing import List, Optional


class Gateway(BaseModel):
    id: int
    gateway_name: str = Field(alias='gatewayname')
    address: str
    latitude: Optional[str]
    longitude: Optional[str]
    communication_type: str = Field(alias='communicationtype')


class GatewayResponse(BaseModel):
    data: List[Gateway]
    status: int
