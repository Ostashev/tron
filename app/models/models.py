import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.core.db import Base


class RequestLog(Base):

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, index=True)
    bandwidth = Column(Float)
    energy = Column(Float)
    trx_balance = Column(Float)
    request_time = Column(DateTime, default=datetime.datetime.utcnow)
