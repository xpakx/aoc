from utils.loader import get_file
from utils.runner import AdventDay
from dataclasses import dataclass
from utils.parser import parse


def load1(filename):
    return get_file(filename, as_int=True)


def part1(nums):
    base = len(nums) + 1
    print(base)
    curr = 2025 % base
    reshaped = [1] + nums[::2] + nums[1::2][::-1]
    print(nums)
    print(reshaped)
    return reshaped[curr]


@dataclass
class Range:
    start: int
    end: int

    def __post_init__(self):
        self.length = self.end - self.start + 1
        self.reversed = False

    def get(self, index: int):
        if self.reversed:
            return self.end - index
        else:
            return self.start + index


def load(filename):
    data = get_file(filename)
    return parse(Range, "{start}-{end}", data)


def part2(ranges):
    first_part = ranges[::2]
    second_part = ranges[1::2][::-1]
    for r in second_part:
        r.reversed = True
    ranges = [Range(1, 1)] + first_part + second_part
    print(ranges)
    base = sum(r.length for r in ranges)
    print(base)
    curr = 20252025 % base
    for r in ranges:
        if curr < r.length:
            return r.get(curr)
        curr -= r.length


app = AdventDay()
app.run()
