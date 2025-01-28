import tronpy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import RequestLog
from app.schemas.tron import Wallet
from app.services.logger import setup_logger

logger = setup_logger("app.services")


async def get_wallet_info(wallet_address: str) -> Wallet:
    logger.info(f"Получение данных аккаунта для адреса {wallet_address}")
    tron = tronpy.Tron()
    try:
        account = tron.get_account(wallet_address)
        balance = account['balance'] / 10 ** 6

        bandwidth = account.get('bandwidth', 0)
        energy = account.get('energy', 0)
        trx_balance = balance

        logger.info(f"Данные аккаунта получены: bandwidth={bandwidth}, energy={energy}, trx_balance={trx_balance}")
        return Wallet(bandwidth=bandwidth, energy=energy, trx_balance=trx_balance)
    except Exception as e:
        logger.error(f"Ошибка получения данных аккаунта для {wallet_address}: {e}")
        raise


async def log_request(wallet_address, bandwidth, energy, trx_balance, session: AsyncSession):
    logger.info(
        f"Логирование запроса: {wallet_address}, bandwidth={bandwidth}, energy={energy}, trx_balance={trx_balance}")
    try:
        db_log = RequestLog(wallet_address=wallet_address, bandwidth=bandwidth, energy=energy, trx_balance=trx_balance)
        session.add(db_log)
        await session.commit()
        await session.refresh(db_log)
        logger.info(f"Запись успешно сохранена в базе данных: {db_log}")
        return db_log
    except Exception as e:
        logger.error(f"Ошибка при логировании запроса: {e}")
        raise


async def get_log(skip: int, limit: int, session: AsyncSession):
    logger.info(f"Получение записей с параметрами: skip={skip}, limit={limit}")
    try:
        logs = await session.execute(select(RequestLog).offset(skip).limit(limit))
        logs = logs.scalars().all()
        logger.info(f"Получено {len(logs)} записей из базы данных.")
        return logs
    except Exception as e:
        logger.error(f"Ошибка при получении записей: {e}")
        raise
