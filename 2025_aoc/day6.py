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


def load2(filename):
    lines = get_file(filename, strip=False)
    ns = lines[:-1]
    ops = lines[-1]
    data = []
    ln = max([len(x) for x in lines])
    nums = []
    op = ' '
    for i in range(ln):
        c = []
        for n in ns:
            c.append(n[i])
        cop = ops[i] if i < len(ops) else ' '
        if cop != ' ':
            op = cop
        num = ''.join(c).strip()
        if num == '':
            data.append(Entry(nums=nums, op=op))
            nums = []
        else:
            nums.append(int(num))
    if len(nums) > 0:
        data.append(Entry(nums=nums, op=op))
        nums = []
    return data


def task1(data):
    return sum(entry.result() for entry in data)


def task2(data):
    return sum(entry.result() for entry in data)


app = AdventDay()
app.run(test=False)
