import asyncio
import logging

logger = logging.getLogger(__name__)

class AsyncScheduler:
    """Асинхронный планировщик задач."""
    def __init__(self, storage):
        self.storage = storage

    async def run_all(self):
        tasks = []
        for t in self.storage:
            if asyncio.iscoroutinefunction(t.run):
                tasks.append(asyncio.create_task(t.run()))
            else:
                loop = asyncio.get_event_loop()
                tasks.append(loop.run_in_executor(None, t.run))
        await asyncio.gather(*tasks)
        logger.info("Все асинхронные задачи завершены.")
