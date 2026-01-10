from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename)


def task1(data):
    print(data)


app = AdventDay()
app.run()
