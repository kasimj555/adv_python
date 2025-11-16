import functools
import time
import logging

logger = logging.getLogger(__name__)

def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug("Calling %s with args=%s kwargs=%s", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        logger.debug("%s returned %r", func.__name__, result)
        return result
    return wrapper


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.perf_counter()
            logger.info("%s took %.6f seconds", func.__name__, end - start)
    return wrapper


# Асинхронные версии декораторов

def async_timeit(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return await func(*args, **kwargs)
        finally:
            end = time.perf_counter()
            logger.info("%s took %.6f seconds", func.__name__, end - start)
    return wrapper


def async_log_call(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.debug("Calling async %s with args=%s kwargs=%s", func.__name__, args, kwargs)
        result = await func(*args, **kwargs)
        logger.debug("async %s returned %r", func.__name__, result)
        return result
    return wrapper