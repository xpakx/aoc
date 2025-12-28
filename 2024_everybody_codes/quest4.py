from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename, as_int=True)


def task1(data):
    m = min(data)
    return sum([x - m for x in data])


def task2(data):
    return task1(data)


def task3(data):
    data.sort()
    middle = len(data) // 2
    median = data[middle]
    return sum([abs(x - median) for x in data])


app = AdventDay()
app.run()
