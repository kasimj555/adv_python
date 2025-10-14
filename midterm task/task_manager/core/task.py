from dataclasses import dataclass, field
import asyncio
import time
from task_manager.utils.decorators import log_execution
from task_manager.core.metaclass import TaskMeta


@dataclass(order=True)
class BaseTask(metaclass=TaskMeta):
    priority: int
    id: str = field(compare=False, default="")
    completed: bool = field(compare=False, default=False)
    duration: float = field(compare=False, default=0.3)

    def run(self):
        raise NotImplementedError


@dataclass(order=True)
class SyncTask(BaseTask):
    @log_execution
    def run(self):
        """Синхронная задача — имитация работы через time.sleep."""
        time.sleep(self.duration)
        self.completed = True
        return f"SyncTask {self.id} done"


@dataclass(order=True)
class AsyncTask(BaseTask):
    @log_execution
    async def run(self):
        """Асинхронная задача — имитация работы через asyncio.sleep."""
        await asyncio.sleep(self.duration)
        self.completed = True
        return f"AsyncTask {self.id} done"
