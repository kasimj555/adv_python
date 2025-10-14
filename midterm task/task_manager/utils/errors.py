class TaskManagerError(Exception):
    """Ошибка менеджера задач."""
    pass

class TaskExecutionError(TaskManagerError):
    """Ошибка выполнения задачи."""
    pass
