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


app = AdventDay()
app.run()
