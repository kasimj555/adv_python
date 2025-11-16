Генератор логов

В отдельном терминале запускаем генератор логов:
    python scripts/log_generator.py
Каждые 0.3 секунды добавляется новая строка в sample.log.
Пример вывода генератора:
    Wrote: 2025-11-16 22:00:01 [INFO] Test log message 0
    Wrote: 2025-11-16 22:00:01 [WARNING] Test log message 1


Запуск анализатора

Асинхронный режим
Команда для запуска
    python -m async_log_analyzer.main sample.log --mode async --runtime 20
--mode async — асинхронное неблокирующее чтение
--runtime 20 — время работы анализатора в секундах
Вывод каждые 5 секунд:
    INFO:root:Periodic report: [('INFO', 12), ('WARNING', 5), ('ERROR', 3)]

Синхронный режим
Команда для запуска
    python -m async_log_analyzer.main sample.log --mode sync --runtime 20
Чтение построчно через генератор Python
Периодические отчёты каждые 5 секунд:
    INFO:__main__:Periodic report: [('WARNING', 1007), ('INFO', 953), ('ERROR', 946)]

Многопоточный режим
Команда для запуска
    python -m async_log_analyzer.main sample.log --mode thread --runtime 20
Несколько потоков (ThreadPoolExecutor) читают лог параллельно
Итоговый отчёт после завершения:
    INFO:__main__:Threaded run report: [('WARNING', 4216), ('INFO', 4036), ('ERROR', 3976)]
