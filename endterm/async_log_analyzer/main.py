import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from async_log_analyzer.parser import tail_file_async, tail_file_sync
from async_log_analyzer.analyzer import LogStats
from async_log_analyzer.decorators import async_timeit, timeit

logger = logging.getLogger(__name__)

async def async_reader(path, stats: LogStats, interval=0.1):
    async for entry in tail_file_async(path):
        if entry is None:
            await asyncio.sleep(interval)
            continue
        stats.feed(entry)


async def periodic_report(stats: LogStats, period=5):
    while True:
        await asyncio.sleep(period)
        top = stats.most_common()
        logger.info("Periodic report: %s", top)


@async_timeit
async def run_async(path, runtime=15):
    stats = LogStats()
    reader_task = asyncio.create_task(async_reader(path, stats))
    reporter_task = asyncio.create_task(periodic_report(stats, period=5))
    await asyncio.sleep(runtime)
    reader_task.cancel()
    reporter_task.cancel()
    try:
        await reader_task
    except asyncio.CancelledError:
        pass
    try:
        await reporter_task
    except asyncio.CancelledError:
        pass
    return stats

@timeit
def run_sync(path, runtime=15):
    stats = LogStats()
    generator = tail_file_sync(path)
    start = time.time()
    last_report = start
    try:
        while time.time() - start < runtime:
            item = next(generator)
            if item is None:
                time.sleep(0.1)
                continue
            stats.feed(item)

            # Периодический отчёт каждые 5 секунд
            if time.time() - last_report >= 5:
                logger.info("Periodic report: %s", stats.most_common())
                last_report = time.time()
    except StopIteration:
        pass
    return stats


@timeit
def run_threaded(path, runtime=15, workers=4):
    stats = LogStats()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(_thread_worker, path, runtime) for _ in range(workers)]
        for f in futures:
            partial_stats = f.result()
            stats.counter.update(partial_stats.counter)
    logger.info("Threaded run report: %s", stats.most_common())
    return stats


def _thread_worker(path, runtime):
    stats = LogStats()
    gen = tail_file_sync(path)
    start = time.time()
    try:
        while time.time() - start < runtime:
            item = next(gen)
            if item is None:
                import time as _t
                _t.sleep(0.05)
                continue
            stats.feed(item)
    except StopIteration:
        pass
    return stats


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import argparse

    parser = argparse.ArgumentParser(description="Async Log Analyzer")
    parser.add_argument("path", help="Path to log file to tail")
    parser.add_argument("--mode", choices=["async", "sync", "thread"], default="async")
    parser.add_argument("--runtime", type=int, default=30)
    args = parser.parse_args()

    if args.mode == "async":
        asyncio.run(run_async(args.path, runtime=args.runtime))
    elif args.mode == "sync":
        run_sync(args.path, runtime=args.runtime)
    else:
        run_threaded(args.path, runtime=args.runtime)