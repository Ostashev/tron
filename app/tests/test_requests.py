from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RequestLog
from app.services.tron import log_request


@pytest.mark.asyncio
@patch('app.services.tron.get_log')
async def test_get_request_logs(mock_get_log):
    # Мокируем ответ от get_log
    mock_get_log.return_value = [
        {
            'id': 1,
            'wallet_address': 'TDQnQ6WjEJjXLsXLPo3sqmzFhgybQXwBgk',
            'bandwidth': 1000,
            'energy': 2000,
            'trx_balance': 50.0,
            'request_time': '2025-01-25T00:00:00'
        },
        {
            'id': 2,
            'wallet_address': 'TDQnQ6WjEJjXLsXLPo3sqmzFhgybQXwBgk',
            'bandwidth': 500,
            'energy': 1500,
            'trx_balance': 30.0,
            'request_time': '2025-01-24T00:00:00'
        }
    ]

    # Используем AsyncClient для тестов
    async with AsyncClient(base_url="http://127.0.0.1:8089") as ac:
        response = await ac.get('/tron/requests')

    assert response.status_code == 200


@pytest.mark.asyncio
@patch('app.services.tron.get_wallet_info', new_callable=AsyncMock)
@patch('app.services.tron.log_request', new_callable=AsyncMock)
async def test_get_wallet_data(mock_log_request, mock_get_wallet_info):
    # Мокируем ответ для log_request
    mock_log_request.return_value = {
        'id': 1,
        'wallet_address': 'TDQnQ6WjEJjXLsXLPo3sqmzFhgybQXwBgk',
        'bandwidth': 1000,
        'energy': 2000,
        'trx_balance': 50.0,
        'request_time': '2025-01-25T00:00:00'
    }

    # Мокируем асинхронный ответ для get_wallet_info
    mock_get_wallet_info.return_value = {
        'bandwidth': 1000,
        'energy': 2000,
        'trx_balance': 50.0
    }

    # Данные для теста
    test_wallet_address = {
        "wallet_address": "TDQnQ6WjEJjXLsXLPo3sqmzFhgybQXwBgk"
    }

    # Выполняем запрос с помощью AsyncClient
    async with AsyncClient(base_url="http://127.0.0.1:8089") as ac:
        response = await ac.post('/tron/wallet', json=test_wallet_address)

    # Проверяем статус ответа
    assert response.status_code == 201
    # Преобразуем тело ответа в JSON
    response_json = response.json()

    # Проверяем, что в ответе есть необходимые поля
    assert 'bandwidth' in response_json
    assert 'energy' in response_json
    assert 'trx_balance' in response_json


@pytest.mark.asyncio
async def test_log_request():
    # Мокаем сессию базы данных
    mock_session = AsyncMock(spec=AsyncSession)

    # Создаем реальный объект RequestLog
    mock_db_log = RequestLog(wallet_address='', bandwidth=0, energy=0, trx_balance=0)

    # Присваиваем значения для mock_db_log
    mock_db_log.wallet_address = 'Тестовый номер'
    mock_db_log.bandwidth = 1000
    mock_db_log.energy = 2000
    mock_db_log.trx_balance = 50.0

    # Мокаем методы сессии
    mock_session.add = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock(return_value=mock_db_log)

    # Параметры для вызова функции
    wallet_address = 'Тестовый номер'
    bandwidth = 1000
    energy = 2000
    trx_balance = 50.0

    # Вызываем саму функцию
    result = await log_request(wallet_address, bandwidth, energy, trx_balance, mock_session)

    # Проверяем, что методы сессии были вызваны
    mock_session.add.assert_called_once()
    # Проверяем, что commit был вызван
    mock_session.commit.assert_called_once()

    # Проверяем, что refresh был вызван с объектом RequestLog
    mock_session.refresh.assert_called_once()

    # Проверяем, что значения полей совпадают
    assert result.wallet_address == mock_db_log.wallet_address
    assert result.bandwidth == mock_db_log.bandwidth
    assert result.energy == mock_db_log.energy
    assert result.trx_balance == mock_db_log.trx_balance
