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


def task2(steps):
    pos = 50
    result = 0
    for step in steps:
        last = pos
        pos_temp = pos + step[0]*step[1]
        pos = pos_temp % 100
        passes = abs(pos_temp - pos) // 100
        result += passes
        if pos == 0 and step[0] < 0:
            result += 1
        if last == 0 and step[0] < 0:
            result -= 1
    return result


app = AdventDay()
app.run()
