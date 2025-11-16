import time
import random

def generate_logs(path="sample.log", delay=0.2):
    """
    Простой генератор логов
    Каждые delay секунд добавляет новую строку в файл
    """
    levels = ["INFO", "WARNING", "ERROR"]
    i = 0
    with open(path, "a", encoding="utf-8") as f:
        while True:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            line = f"{timestamp} [{random.choice(levels)}] Test log message {i}\n"
            f.write(line)
            f.flush()
            print("Wrote:", line.strip())
            i += 1
            time.sleep(delay)


if __name__ == "__main__":
    generate_logs("sample.log", delay=0.3)
