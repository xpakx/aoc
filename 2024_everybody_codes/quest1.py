from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename, split_lines=False)


def task1(data):
    return data.count("B") + 3*data.count("C")


app = AdventDay()
app.run()
