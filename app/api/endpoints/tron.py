from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.tron import RequestLogSchema, WalletAddress, WalletInfo
from app.services.logger import main_logger
from app.services.tron import get_log, get_wallet_info, log_request

router = APIRouter()
logger = main_logger


@router.post("/wallet",
             response_model=RequestLogSchema,
             status_code=status.HTTP_201_CREATED,
             summary='Запрос иформации по кошельку.',
             )
async def get_wallet_data(
        wallet_address: WalletAddress,
        db: AsyncSession = Depends(get_async_session)
) -> RequestLogSchema:
    logger.info(f"Получение данных для кошелька: {wallet_address.wallet_address}")
    wallet_info = await get_wallet_info(wallet_address.wallet_address)
    log = await log_request(
        wallet_address.wallet_address, wallet_info.bandwidth, wallet_info.energy, wallet_info.trx_balance, db)
    logger.info(f"Запрос успешно записан в бд: {log}")
    return log


@router.get("/requests",
            response_model=List[WalletInfo],
            status_code=status.HTTP_200_OK,
            summary='Получить список запросов.',
            )
async def get_request_logs(
        skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_session)) -> List[WalletInfo]:
    logger.info(f"Получение списка запросов с параметрами skip={skip}, limit={limit}")
    logs = await get_log(skip, limit, db)
    logger.info(f"Получено {len(logs)} записей.")
    return logs
