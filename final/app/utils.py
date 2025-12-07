import logging
from contextlib import contextmanager
import time

def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
    level=level,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",)

@contextmanager
def timing(name: str):
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        logging.getLogger(name).info("Elapsed: %.6f s", elapsed)