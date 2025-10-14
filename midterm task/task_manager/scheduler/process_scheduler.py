import multiprocessing
import logging
import time
from task_manager.utils.errors import TaskExecutionError

logger = logging.getLogger(__name__)

class ProcessScheduler:
    """Планировщик для выполнения задач в отдельных процессах."""

    def __init__(self, storage):
        self.storage = storage
        self.processes = []

    @staticmethod
    def _run_task(task):
        try:
            logger.info(f"Процесс {multiprocessing.current_process().name}: выполняется {task.id}")
            time.sleep(0.5)
            task.run()
            logger.info(f"Процесс {multiprocessing.current_process().name}: завершена {task.id}")
        except Exception as e:
            logger.error(f"Ошибка в задаче {task.id}: {e}")
            raise TaskExecutionError(f"Ошибка выполнения задачи {task.id}") from e

    def run_all(self):
        for task in self.storage:
            process = multiprocessing.Process(target=self._run_task, args=(task,))
            self.processes.append(process)
            process.start()

        for process in self.processes:
            process.join()

        logger.info("Все процессы завершены.")
