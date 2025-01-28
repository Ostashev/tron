# TRON


## Стек технологий
- **FastAPI**: для разработки REST API
- **PostgreSQL**: база данных для хранения информации о запросах
- **Docker**: контейнеризация для упрощения развёртывания

## Установка и запуск

Содержание`.env` файла:
   ```env
   APP_TITLE=TPOH
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@tron_db:5432/tron
   SECRET=трон
   API_ROOT_PATH=/
   ```

   Склонируйте репозиторий:
   ```git clone git@github.com:Ostashev/tron.git```

   Перейдите в дирректорию:
   ```cd tron```

   Запустите контейнеры:
   ```docker-compose up --build```

   После успешного запуска, сервер API будет доступен по адресу:
   ```http://localhost:8089```
