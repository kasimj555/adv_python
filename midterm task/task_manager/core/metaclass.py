class TaskMeta(type):
    """Метакласс, проверяющий наличие метода run."""
    def __new__(cls, name, bases, attrs):
        if "run" not in attrs and not any(hasattr(b, "run") for b in bases):
            raise TypeError(f"Класс {name} должен реализовать метод run()")
        return super().__new__(cls, name, bases, attrs)
