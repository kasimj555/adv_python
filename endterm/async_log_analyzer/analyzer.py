from collections import Counter
from .decorators import log_call

class LogStats:
    def __init__(self):
        self.counter = Counter()

    @log_call
    def feed(self, log_line):
        if log_line is None:
            return
        self.counter[log_line.level] += 1

    def most_common(self, n=10):
        return self.counter.most_common(n)

    def reset(self):
        self.counter.clear()