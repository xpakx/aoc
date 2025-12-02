from utils.loader import get_file
from utils.parser import parse
from utils.runner import AdventDay
from dataclasses import dataclass
import re


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
            test = re.search(r"^(.+)\1$", num)
            if test:
                result += i
    return result


app = AdventDay()
app.run()
