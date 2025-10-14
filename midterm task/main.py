import asyncio
import logging
from task_manager.core.task import AsyncTask, SyncTask
from task_manager.storage.task_storage import TaskStorage
from task_manager.generators.task_generator import task_filter
from task_manager.scheduler.async_scheduler import AsyncScheduler
from task_manager.scheduler.thread_scheduler import ThreadScheduler
from task_manager.scheduler.process_scheduler import ProcessScheduler
from task_manager.utils.errors import TaskManagerError
from task_manager.generators.task_iterator import TaskIterator

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

async def main():
    storage = TaskStorage()

    print("Введите задачи (тип: async/sync, id, приоритет). Пустая строка завершение.")
    while True:
        try:
            line = input("→ ").strip()
            if not line:
                break
            parts = line.split()
            if len(parts) != 3:
                print("Формат: <тип> <id> <приоритет>")
                continue
            ttype, tid, prio = parts[0], parts[1], int(parts[2])
            if ttype == "async":
                storage.push(AsyncTask(id=tid, priority=prio))
            elif ttype == "sync":
                storage.push(SyncTask(id=tid, priority=prio))
            else:
                print("Неизвестный тип задачи (используйте async/sync)")
        except ValueError:
            print("Ошибка: приоритет должен быть числом")
        except Exception as e:
            print(f"Ошибка добавления задачи: {e}")

    print(f"\nВсего задач: {len(storage._heap)}")

    print("\n---Перебор всех задач итератором---")
    for task in TaskIterator(storage._heap):
        print(f"Task {task.id}, priority {task.priority}")

    print("\n---Фильтрация задач (priority >= 2) ---")
    try:
        for t in task_filter((task for _, task in storage._heap), 2):
            print(f"Task {t.id}, priority {t.priority}")
    except Exception as e:
        print(f"Ошибка фильтрации: {e}")

    print("\n---Асинхронное выполнение задач---")
    try:
        async_scheduler = AsyncScheduler(storage)
        await async_scheduler.run_all()
    except TaskManagerError as e:
        print(f"Ошибка асинхронного выполнения: {e}")

    print("\n---Многопоточность---")
    try:
        thread_scheduler = ThreadScheduler(storage)
        thread_scheduler.run_all()
    except Exception as e:
        print(f"Ошибка при многопоточном запуске: {e}")

    print("\n---Мультипроцессинг---")
    try:
        process_scheduler = ProcessScheduler(storage)
        process_scheduler.run_all()
    except Exception as e:
        print(f"[!] Ошибка при мультипроцессорном запуске: {e}")

    print("\n--- Завершение программы ---")

if __name__ == "__main__":
    asyncio.run(main())
