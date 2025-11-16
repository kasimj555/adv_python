import aiofiles
import asyncio
import re
from collections import namedtuple
from .exceptions import InvalidLogFormatError, FileReadError

LogLine = namedtuple("LogLine", ["timestamp", "level", "message"])

LOG_PATTERN = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+\[(?P<level>ERROR|WARNING|INFO)\]\s+(?P<msg>.*)$"
)

def parse_line(line: str) -> LogLine:
    match = LOG_PATTERN.match(line.strip())
    if not match:
        raise InvalidLogFormatError(f"Line does not match expected format: {line!r}")
    return LogLine(timestamp=match.group("ts"), level=match.group("level"), message=match.group("msg"))

async def tail_file_async(path):
    try:
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            while True:
                line = await f.readline()
                if not line:
                    await asyncio.sleep(0.1)
                    continue
                try:
                    yield parse_line(line)
                except InvalidLogFormatError:
                    continue
    except OSError as e:
        raise FileReadError(str(e))

def tail_file_sync(path):
    import time
    try:
        with open(path, "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                try:
                    yield parse_line(line)
                except InvalidLogFormatError:
                    continue
    except OSError as e:
        raise FileReadError(str(e))
