import math
from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename, as_int=True)


def load3(filename):
    data = get_file(filename)
    chain = map(lambda n: [int(x) for x in n.split('|')], data[1:-1])
    return int(data[0]), list(chain), int(data[-1])


def task1(data):
    print(data)
    rot = 2025
    ratio = data[0]/data[-1]
    return math.floor(rot*ratio)


def task2(data):
    ratio = data[0]/data[-1]
    return math.ceil(10000000000000/ratio)


def task3(start, chain, end):
    ratios = map(lambda e: e[1]/e[0], chain)
    ratio_mult = math.prod(ratios)
    ratio = start/end
    return math.floor(ratio * ratio_mult * 100)


app = AdventDay()
app.run()
