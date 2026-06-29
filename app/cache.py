import os
import redis
import json
from typing import Any

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses = True)

def set_cache(key: str, value: Any, ttl: int = 300):
    try:
        json_value = json.dumps(value, ensure_ascii=False)
        redis_client.setex(key, ttl, json_value)
    except Exception as e:
        print(f"Во время добавления кэша произошла ошибка {e}")

def get_cache(key):
    try:
        cached = redis_client.get(key)
        if cached is None:
            return None
        return json.loads(cached)    
    except Exception as e:
        print(f"Во время получения кэша произошла ошибка {e}")

def delete_cache(key):
    try:
        redis_client.delete(key)
    except Exception as e:
        print(f"Во время удаления кэша произошла ошибка {e}")