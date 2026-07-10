import os
import redis
import json
from typing import Any
import logging

# Настраиваем логгер
logger = logging.getLogger(__name__)

# Получаем REDIS_URL из переменных окружения
REDIS_URL = os.getenv('REDIS_URL')

# Пытаемся подключиться к Redis, но не падаем если не получается
redis_client = None
redis_available = False

if REDIS_URL:
    try:
        redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        # Проверяем подключение
        redis_client.ping()
        redis_available = True
        logger.info("✅ Redis подключен успешно")
    except Exception as e:
        logger.warning(f"⚠️ Redis недоступен: {e}. Кэширование отключено.")
        redis_client = None
        redis_available = False
else:
    logger.info("ℹ️ REDIS_URL не задан. Кэширование отключено.")

def set_cache(key: str, value: Any, ttl: int = 300):
    """Добавляет значение в кэш. Если Redis недоступен - просто пропускает."""
    if not redis_available or redis_client is None:
        return
    
    try:
        json_value = json.dumps(value, ensure_ascii=False)
        redis_client.setex(key, ttl, json_value)
    except Exception as e:
        logger.error(f"Ошибка при добавлении кэша: {e}")

def get_cache(key: str):
    """Получает значение из кэша. Если Redis недоступен - возвращает None."""
    if not redis_available or redis_client is None:
        return None
    
    try:
        cached = redis_client.get(key)
        if cached is None:
            return None
        return json.loads(cached)    
    except Exception as e:
        logger.error(f"Ошибка при получении кэша: {e}")
        return None

def delete_cache(key: str):
    """Удаляет значение из кэша. Если Redis недоступен - просто пропускает."""
    if not redis_available or redis_client is None:
        return
    
    try:
        redis_client.delete(key)
    except Exception as e:
        logger.error(f"Ошибка при удалении кэша: {e}")