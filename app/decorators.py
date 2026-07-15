import logging
import functools
import time
import asyncio

logger = logging.getLogger(__name__)

def log_function_call(func):
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        logger.info(f"Вызвана async функция {func.__name__} с аргументами {args} {kwargs}")
        result = await func(*args, **kwargs)
        logger.info(f" async Функция {func.__name__} вернула {result}")
        return result
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        logger.info(f"Вызвана sync функция {func.__name__} с аргументами {args} {kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"sync Функция {func.__name__} вернула {result}")
        return result
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
    

def log_execution_time(func):
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(f"async Функция {func.__name__} выполнилась за {end - start} секунд.")
        return result
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(f"sync Функция {func.__name__} выполнилась за {end - start} секунд")
        return result
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper