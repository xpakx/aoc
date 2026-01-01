from utils.loader import get_file
from utils.runner import AdventDay
from functools import cache


def load(filename):
    return get_file(filename, as_int=True)


def get_stamp(brigthness, stamps):
    for i, stamp in enumerate(stamps):
        if brigthness < stamp:
            return stamps[i-1]
    return stamps[i]


def stamps_for(brigthness, stamps):
    used = []
    while brigthness > 0:
        stamp = get_stamp(brigthness, stamps)
        brigthness -= stamp
        used.append(stamp)
    return used


def task1(brightness):
    stamps = [1, 3, 5, 10]
    result = 0
    for b in brightness:
        s = stamps_for(b, stamps)
        print(b, s)
        result += len(s)
    return result


@cache
def stamps_for2(brightness, stamps):
    if brightness == 0:
        return 0
    if brightness < 0:
        return 10**100
    best = 10**100
    for stamp in stamps:
        sub = stamps_for2(brightness - stamp, stamps)
        best = min(best, 1 + sub)
    return best


def task2(brightness):
    stamps_for2.cache_clear()
    stamps = [
            1, 3, 5, 10, 15, 16, 20, 24, 25, 30
    ]
    stamps.reverse()
    stamps = tuple(stamps)
    result = 0
    for b in brightness:
        result += stamps_for2(b, stamps)
    return result


def count_split(brightness, stamps):
    half = brightness // 2
    rest = brightness - half
    min = 9999999
    for i in range(51 - brightness % 2):
        first = stamps_for2(half-i, stamps)
        second = stamps_for2(rest+i, stamps)
        result = first + second
        if result < min:
            min = result
    return min


def task3(brightness):
    stamps_for2.cache_clear()
    stamps = [
            1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101
    ]
    stamps.reverse()
    stamps = tuple(stamps)
    result = 0
    for b in brightness:
        result += count_split(b, stamps)
    return result


app = AdventDay()
app.run()
