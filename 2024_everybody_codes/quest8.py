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


app = AdventDay()
app.run()
