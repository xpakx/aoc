from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename, split_lines=False)


def task1(data):
    return data.count("B") + 3*data.count("C")


def cost_of(insect):
    if insect == 'B':
        return 1
    if insect == 'C':
        return 3
    if insect == 'D':
        return 5
    return 0


def task2(data):
    result = 0
    for first, second in zip(data[::2], data[1::2]):
        result += cost_of(first) + cost_of(second)
        if first != 'x' and second != 'x':
            result += 2
    return result


def is_empty(insect):
    return insect == 'x'


def task3(data):
    result = 0
    for first, second, third in zip(data[::3], data[1::3], data[2::3]):
        result += cost_of(first) + cost_of(second) + cost_of(third)
        insects = sum([not is_empty(i) for i in [first, second, third]])
        if insects == 2:
            result += 2
        elif insects == 3:
            result += 6
    return result


app = AdventDay()
app.run()
