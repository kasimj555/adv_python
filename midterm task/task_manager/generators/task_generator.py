def task_filter(tasks, priority_threshold):
    """Генератор, возвращающий задачи с приоритетом"""
    for t in tasks:
        if t.priority >= priority_threshold:
            yield t
