from utils.loader import get_file
from utils.helpers import transform_steps
from utils.runner import AdventDay


def load(filename):
    data = get_file(filename)
    return transform_steps(data)


def task1(steps):
    pos = 50
    result = 0
    for step in steps:
        pos += step[0]*step[1]
        pos = pos % 100
        if pos == 0:
            result += 1
    return result


app = AdventDay()
app.run()
