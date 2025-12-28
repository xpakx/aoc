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
    a = min(data)
    m = max(data)
    minimum = m*len(data)
    for i in range(a, m+1):
        t = sum([abs(x - i) for x in data])
        if t < minimum:
            minimum = t
    return minimum


app = AdventDay()
app.run()
