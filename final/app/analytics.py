import timeit
import cProfile
import pstats
from io import StringIO
from typing import Iterable, Dict, Any, Callable

def time_compare(funcs: Dict[str, Callable], number: int = 1000) -> Dict[str, float]:
    """Сравнивает время выполнения timeit
    Возвращает среднее время функции"""
    results = {}
    for name, f in funcs.items():
        timer = timeit.Timer(lambda: f())
        total = timer.timeit(number=number)
        results[name] = total / number
    return results

def profile_function(func: Callable, *args, **kwargs) -> str:
    """Профилирует функцию с cProfile и возвращает отчет"""
    pr = cProfile.Profile()
    pr.enable()
    func(*args, **kwargs)
    pr.disable()
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats(20)
    return s.getvalue()

def student_generator(rows: Iterable[Dict[str, Any]]):
    for r in rows:
        yield {"id": int(r["id"]), "name": r["name"], "score": float(r["score"]), "group": r.get("group")}