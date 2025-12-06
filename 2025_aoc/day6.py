from utils.loader import get_file
from utils.runner import AdventDay
from dataclasses import dataclass
from functools import reduce
import operator


@dataclass
class Entry:
    nums: list[int]
    op: str

    def result(self):
        if self.op == '+':
            return sum(self.nums)
        else:
            return reduce(operator.mul, self.nums, 1)


def load1(filename):
    lines = get_file(filename)
    data = []
    for line in lines:
        data.append(line.split())
    data = list(zip(*data))
    d = []
    for elem in data:
        nums = list(map(int, elem[:-1]))
        d.append(Entry(nums=nums, op=elem[-1]))
    return d


def task1(data):
    return sum(entry.result() for entry in data)


app = AdventDay()
app.run(test=False)
