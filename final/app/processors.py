from functools import reduce
from typing import Callable, Iterable, List, Dict, Any, Type

class AutoRegisterMeta(type):
    """Метакласс"""
    registry: Dict[str, Type] = {}

    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        if name != "BaseProcessor":
            AutoRegisterMeta.registry[name] = cls
        return cls


class BaseProcessor(metaclass=AutoRegisterMeta):
    def process(self, data: Iterable[Dict[str, Any]]) -> Any:
        raise NotImplementedError


class AverageScoreProcessor(BaseProcessor):
    """Вычисляет средний балл"""

    def process(self, data: Iterable[Dict[str, Any]]) -> float:
        scores = list(map(lambda r: float(r["score"]), data))
        if not scores:
            return 0.0
        return reduce(lambda a, b: a + b, scores) / len(scores)


class GroupFilterProcessor(BaseProcessor):
    """Фильтрует студентов"""

    def __init__(self, group_name: str):
        self.group_name = group_name

    def process(self, data: Iterable[Dict[str, Any]]) -> List[str]:
        filtered = filter(lambda r: r.get("group") == self.group_name, data)
        return list(map(lambda r: r["name"], filtered))


# Пример функции высшего порядка
def apply_processor(processor_factory: Callable[[], BaseProcessor], data: Iterable[Dict[str, Any]]):
    """Создает процессор через фабрику и применяет его к данным"""
    proc = processor_factory()
    return proc.process(data)