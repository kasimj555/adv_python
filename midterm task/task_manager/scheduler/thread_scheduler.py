import threading
import logging

logger = logging.getLogger(__name__)

class ThreadScheduler:
    """Планировщик для многопоточного выполнения задач."""
    def __init__(self, storage):
        self.storage = storage
        self.threads = []

    def run_all(self):
        for t in self.storage:
            thread = threading.Thread(target=t.run)
            self.threads.append(thread)
            thread.start()
        for thread in self.threads:
            thread.join()
        logger.info("Все потоки завершены.")
    