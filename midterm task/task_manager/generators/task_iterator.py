class TaskIterator:
    """Итератор."""
    def __init__(self, tasks):
        self._tasks = list(tasks)
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._tasks):
            task = self._tasks[self._index]
            self._index += 1
            return task[1] if isinstance(task, tuple) else task
        raise StopIteration
