# Task 1.1
print("#------------#\nTask1.1")
class Countdown:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        self.current = self.n
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val


for num in Countdown(5):
    print(num)


#Task 1.2
print("#------------#\nTask1.2")
def even_numbers(limit):
    for i in range(0, limit + 1, 2):
        yield i

for num in even_numbers(11):
    print(num)


#Task 1.3
print("#------------#\nTask1.3")
def infinite_cycle(lst):
    while True:
        for item in lst:
            yield item

cycle = infinite_cycle([1, 2, 3])
print(next(cycle))
print(next(cycle))
print(next(cycle))
print(next(cycle))
print(next(cycle))


#Task 2.1
print("#------------#\nTask2.1")
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Вызов функции {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def hello():
    print("Привет")

hello()


#Task 2.2
print("#------------#\nTask2.2")
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def hi():
    print("Hi!")

hi()


#Task 2.3
print("#------------#\nTask2.3")
class AutoStr(type):
    def __new__(cls, name, bases, dct):
        if "__str__" not in dct:
            def __str__(self):
                return f"{self.__class__.__name__} {self.__dict__}"
            dct["__str__"] = __str__
        return super().__new__(cls, name, bases, dct)

class Person(metaclass=AutoStr):
    def __init__(self, name, age):
        self.name = name
        self.age = age

print(Person("Alex", 20))


#Task 3.1
print("#------------#\nTask3.1")
from math_utils import add, mul

print(add(2, 3))
print(mul(4, 5))


#Task 3.2
print("#------------#\nTask3.2")
from shapes import area_circle, area_square

print(area_circle(3))
print(area_square(4))


#Task 4.1
print("#------------#\nTask4.1")
from collections import Counter

s = "hello world"
print(Counter(s))


#Task 4.2
print("#------------#\nTask4.2")
from collections import defaultdict
students = [("Иван", 1), ("Алина", 2), ("Макс", 1)]

groups = defaultdict(list)
for name, course in students:
    groups[course].append(name)

print(dict(groups))


#Task 4.3
print("#------------#\nTask4.3")
from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    year: int

books = [
    Book("Война и мир", "Лев Толстой", 1869),
    Book("Мастер и Маргарита", "Михаил Булгаков", 1967),
    Book("Преступление и наказание", "Фёдор Достоевский", 1866),
    Book("Анна Каренина", "Лев Толстой", 1877),
]

books_sorted = sorted(books, key=lambda b: b.year)

for b in books_sorted:
    print(f"{b.year}: {b.title} - {b.author}")