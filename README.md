# FakeStore Backend

Backend для интернет-магазина с аутентификацией, корзиной покупок и кэшированием.

## 🚀 Возможности

- **Аутентификация** - регистрация, вход, JWT токены
- **Каталог товаров** - просмотр, поиск, добавление товаров
- **Корзина** - добавление/удаление товаров, управление количеством
- **Кэширование** - Redis кэширование для производительности
- **Мониторинг** - метрики Prometheus и Grafana дашборды
- **API документация** - автоматическая документация через Swagger/Redoc

## 📋 Требования

- Python 3.11+
- Docker и Docker Compose (опционально)
- Redis (опционально, для кэширования)

## 🛠️ Быстрый старт

### Вариант 1: Локальная разработка (без Docker)

1. **Клонируйте репозиторий**
```bash
git clone <ваш-репозиторий>
cd fakestore-backend
```

2. **Создайте виртуальное окружение**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Установите зависимости**
```bash
pip install -r requirements.txt
```

4. **Настройте окружение**
```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Откройте .env и настройте под свои нужды
# Для локальной разработки SQLite настроен по умолчанию
```

5. **Запустите сервер**
```bash
# База данных будет создана автоматически при первом запуске
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

6. **Откройте в браузере**
- API документация: http://localhost:8000/docs
- Frontend: http://localhost:8000/index.html

### Вариант 2: Docker (рекомендуется)

1. **Запустите все сервисы**
```bash
docker-compose up -d
```

2. **Проверьте статус**
```bash
docker-compose ps
```

3. **Откройте в браузере**
- Frontend + API: http://localhost:8000
- API документация: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (логин: admin, пароль: admin)

4. **Просмотр логов**
```bash
docker-compose logs -f app
```

5. **Остановка**
```bash
docker-compose down
```

## 🔧 Конфигурация

### Переменные окружения (.env файл)

| Переменная | Описание | Пример |
|------------|----------|--------|
| `DATABASE_URL` | URL базы данных | `sqlite:///./fakestore.db` или `postgresql://user:pass@host:5432/db` |
| `TEST_DATABASE_URL` | URL тестовой базы данных | `sqlite:///./test.db` |
| `SECRET_KEY` | Секретный ключ для JWT | Любая строка (в production используйте сложную!) |
| `REDIS_URL` | URL Redis (опционально) | `redis://localhost:6379/0` |

### Структура проекта

```
fakestore-backend/
├── app/                    # Основное приложение
│   ├── __init__.py
│   ├── main.py            # Точка входа FastAPI
│   ├── database.py        # Настройки базы данных
│   ├── models.py          # Модели SQLAlchemy
│   ├── schemas.py         # Pydantic схемы
│   ├── auth.py            # Аутентификация и JWT
│   ├── cache.py           # Redis кэширование
│   └── routers/           # API маршруты
│       ├── auth.py        # /auth/login, /auth/register
│       ├── products.py    # /products/
│       └── cart.py        # /cart/
├── frontend/              # HTML/CSS/JS фронтенд
│   ├── index.html         # Каталог товаров
│   ├── login.html         # Вход/регистрация
│   ├── cart.html          # Корзина
│   └── style.css          # Стили
├── nginx/                 # Nginx конфигурация
│   └── nginx.conf
├── migrations/            # Alembic миграции
├── tests/                 # Тесты
├── docker-compose.yml     # Docker Compose конфигурация
├── Dockerfile             # Docker образ для приложения
├── requirements.txt       # Python зависимости
└── .env                   # Конфигурационный файл
```

## 📚 API Endpoints

### Аутентификация
- `POST /auth/register` - Регистрация нового пользователя
- `POST /auth/login` - Вход пользователя

### Товары
- `GET /products/` - Получить все товары
- `GET /products/?search=query` - Поиск товаров
- `POST /products/` - Добавить товар (требуется аутентификация)

### Корзина
- `GET /cart/` - Получить содержимое корзины
- `POST /cart/` - Добавить товар в корзину
- `DELETE /cart/{item_id}/` - Удалить товар из корзины

### Другие
- `GET /` - Проверка работоспособности
- `GET /health` - Health check endpoint
- `GET /docs` - Swagger документация
- `GET /redoc` - ReDoc документация
- `GET /metrics` - Prometheus метрики

## 🧪 Тестирование

```bash
# Запустить все тесты
pytest

# Запустить с покрытием
pytest --cov=app

# Запустить конкретный тест
pytest tests/test_auth.py -v
```

## 🔍 Решение проблем

### Ошибка: "Database URL is not set!"
**Решение:** Убедитесь, что файл `.env` существует и содержит `DATABASE_URL`.
```bash
cp .env.example .env
# Отредактируйте .env при необходимости
```

### Ошибка: "Failed to fetch" / "ERR_CONNECTION_REFUSED"
**Причина:** Frontend не может подключиться к API.

**Решения:**
1. Убедитесь, что сервер запущен: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. Проверьте, что frontend и API на одном домене/порте
3. При использовании Docker убедитесь, что контейнеры запущены: `docker-compose up -d`

### CORS ошибки
**Решение:** В текущей версии CORS настроен автоматически. Если возникают проблемы:
1. Проверьте, что nginx запущен и конфигурация применена
2. При запуске без Docker убедитесь, что сервер запущен с `--host 0.0.0.0`

### Redis недоступен
**Сообщение:** "Redis недоступен. Кэширование отключено."

**Решение:**
- Это не критично, приложение продолжит работать без кэширования
- Для включения кэширования установите Redis и задайте `REDIS_URL` в `.env`

## 📈 Мониторинг

### Prometheus
- Доступен по адресу: http://localhost:9090
- Автоматически собирает метрики со всех endpoints

### Grafana
- Доступен по адресу: http://localhost:3000
- Логин: `admin`, пароль: `admin`
- Можно настроить дашборды для визуализации метрик

## 🤝 Вклад в проект

1. Fork репозиторий
2. Создайте ветку (`git checkout -b feature/amazing-feature`)
3. Сделайте изменения (`git commit -m 'Add some amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

MIT License

## 🆘 Поддержка

Если у вас возникли проблемы:
1. Проверьте логи приложения
2. Убедитесь, что все зависимости установлены
3. Проверьте конфигурацию в `.env` файле
4. Убедитесь, что порты не заняты другими приложениями

## 🔄 Миграции базы данных

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Описание изменений"

# Применить миграции
alembic upgrade head

# Откатить миграции
alembic downgrade -1