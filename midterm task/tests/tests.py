import unittest
import asyncio
import time
from task_manager.core.task import AsyncTask, SyncTask
from task_manager.storage.task_storage import TaskStorage
from task_manager.generators.task_generator import task_filter
from task_manager.scheduler.async_scheduler import AsyncScheduler
from task_manager.scheduler.thread_scheduler import ThreadScheduler
from task_manager.scheduler.process_scheduler import ProcessScheduler
from task_manager.utils.errors import TaskManagerError


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """Создаём новое хранилище задач перед каждым тестом."""
        self.storage = TaskStorage()
        self.storage.push(SyncTask(id="s1", priority=2))
        self.storage.push(AsyncTask(id="a1", priority=1))
        self.storage.push(SyncTask(id="s2", priority=3))

    def test_task_storage_order(self):
        """Проверяем, что задачи извлекаются по приоритету."""
        task = self.storage.pop()
        self.assertEqual(task.id, "a1")

    def test_generator_filter(self):
        """Проверяем генератор фильтрации."""
        result = list(task_filter((task for _, task in self.storage._heap), 2))
        self.assertTrue(all(t.priority >= 2 for t in result))
        self.assertEqual(len(result), 2)

    def test_sync_task_run(self):
        """Проверяем синхронное выполнение задачи."""
        task = SyncTask(id="x", priority=1)
        result = task.run()
        self.assertIn("done", result)
        self.assertTrue(task.completed)

    def test_async_task_run(self):
        """Проверяем асинхронное выполнение задачи."""
        async def runner():
            task = AsyncTask(id="y", priority=1)
            result = await task.run()
            self.assertIn("done", result)
            self.assertTrue(task.completed)
        asyncio.run(runner())

    def test_async_scheduler(self):
        """Проверяем выполнение всех задач в асинхронном режиме."""
        async def runner():
            scheduler = AsyncScheduler(self.storage)
            await scheduler.run_all()
        asyncio.run(runner())

    def test_thread_scheduler(self):
        """Проверяем многопоточный планировщик."""
        scheduler = ThreadScheduler(self.storage)
        start = time.perf_counter()
        scheduler.run_all()
        duration = time.perf_counter() - start
        self.assertLess(duration, 2.0)

    def test_process_scheduler(self):
        """Проверяем мультипроцессорный планировщик."""
        scheduler = ProcessScheduler(self.storage)
        scheduler.run_all()

    def test_error_on_empty_pop(self):
        """Проверка корректной обработки ошибок при пустом хранилище."""
        empty_storage = TaskStorage()
        with self.assertRaises(TaskManagerError):
            empty_storage.pop()


if __name__ == '__main__':
    unittest.main()
