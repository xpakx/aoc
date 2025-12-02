from utils.loader import get_file
from utils.parser import parse
from utils.runner import AdventDay
from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int


def load(filename):
    data = get_file(filename, split_lines=False, split_by=',')
    return parse(Range, '{start}-{end}', data)


def task1(data):
    result = 0
    for r in data:
        for i in range(r.start, r.end+1):
            num = str(i)
            length = len(num)
            if length % 2 == 0 and num[:length//2] == num[length//2:]:
                result += i
    return result


def task2(data):
    result = 0
    for r in data:
        for i in range(r.start, r.end+1):
            num = str(i)
            if num in (num + num)[1:-1]:
                result += i
    return result


app = AdventDay()
app.run()
