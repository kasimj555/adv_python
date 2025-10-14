import heapq
from task_manager.utils.errors import TaskManagerError

class TaskStorage:
    """Хранилище задач с приоритетами."""
    def __init__(self):
        self._heap = []

    def push(self, task):
        try:
            heapq.heappush(self._heap, (task.priority, task))
        except Exception as e:
            raise TaskManagerError(f"Ошибка добавления задачи {task.id}: {e}")

    def pop(self):
        try:
            return heapq.heappop(self._heap)[1]
        except IndexError:
            raise TaskManagerError("Хранилище задач пусто")

    def __iter__(self):
        return (task for _, task in sorted(self._heap))
