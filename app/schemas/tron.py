from pydantic import BaseModel
from datetime import datetime


class WalletAddress(BaseModel):
    wallet_address: str


class Wallet(BaseModel):
    bandwidth: float
    energy: float
    trx_balance: float


class RequestLogSchema(BaseModel):
    wallet_address: str
    bandwidth: float
    energy: float
    trx_balance: float

    class Config:
        orm_mode = True


class WalletInfo(RequestLogSchema):
    id: int
    request_time: datetime
