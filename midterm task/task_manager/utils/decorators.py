import asyncio
import logging
import functools

logger = logging.getLogger(__name__)

def log_execution(func):
    """Декоратор для логирования выполнения задачи."""
    if asyncio.iscoroutinefunction(func):
        async def wrapper(*args, **kwargs):
            logger.info(f"Начало {func.__name__}")
            result = await func(*args, **kwargs)
            logger.info(f"Завершение {func.__name__}")
            return result
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Начало {func.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"Завершение {func.__name__}")
            return result
    return wrapper
