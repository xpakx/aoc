from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename, as_int=True)


def task1(data):
    m = min(data)
    return sum([x - m for x in data])


app = AdventDay()
app.run()
