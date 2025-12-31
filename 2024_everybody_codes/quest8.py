from utils.loader import get_file
from utils.runner import AdventDay
from math import sqrt, ceil


def load(filename):
    return get_file(filename, as_int=True)[0]


def task1(data):
    # nth layer needs additonal 2n - 1
    # n-layer building need sum 1 to n 2n-1
    # = 2(1+2...+n) - n
    # = 2*(n(n+1)/2) - n
    # = n(n+1) - n
    # = n^2 +n - n = n^2
    root = ceil(sqrt(data))
    closest_square = root**2
    to_buy = closest_square - data
    floor = 2*(root-1) + 1
    print(to_buy, floor)
    return to_buy*floor


def layer(number, priests, acolytes):
    return (number * priests) % acolytes


def task2(priests):
    blocks = 20240000
    curr = 1
    blocks -= curr
    layer_num = 1
    while blocks > 0:
        layer_num += 1
        curr = layer(curr, priests, 1111)
        blocks_used = 2*layer_num - 1
        blocks -= blocks_used*curr
    floor = 2*(layer_num-1) + 1
    print(-blocks, floor)
    return -blocks*floor


def layer3(number, priests, acolytes):
    return ((number * priests) % acolytes) + acolytes


def to_remove(priests, width, height, acolytes):
    return (priests * width * height) % acolytes


def task3(priests):
    start_blocks = 202400000
    acolytes = 10
    curr = 1
    blocks = start_blocks - curr
    layer_num = 1
    cols = [1]
    while blocks > 0:
        layer_num += 1
        curr = layer3(curr, priests, acolytes)
        blocks_used = 2*layer_num - 1
        blocks -= blocks_used*curr
        cols = [curr] + [x+curr for x in cols] + [curr]
    floor = 2*(layer_num-1) + 1
    cols = [to_remove(priests, floor, x, acolytes) for x in cols]
    # print(cols)
    empty = sum(cols[1:-1])

    return abs(blocks) - empty


app = AdventDay()
app.run()
