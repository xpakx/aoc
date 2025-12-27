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


app = AdventDay()
app.run()
