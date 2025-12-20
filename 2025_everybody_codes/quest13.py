from utils.loader import get_file
from utils.runner import AdventDay
from dataclasses import dataclass
from utils.parser import parse


def load1(filename):
    return get_file(filename, as_int=True)


def part1(nums):
    base = len(nums) + 1
    curr = 2025 % base
    reshaped = [1] + nums[::2] + nums[1::2][::-1]
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


def solve_ranges(ranges: list[Range], steps: int):
    first_part = ranges[::2]
    second_part = ranges[1::2][::-1]
    for r in second_part:
        r.reversed = True
    ranges = [Range(1, 1)] + first_part + second_part
    base = sum(r.length for r in ranges)
    curr = steps % base
    for r in ranges:
        if curr < r.length:
            return r.get(curr)
        curr -= r.length


def part2(ranges):
    return solve_ranges(ranges, 20252025)


def part3(ranges):
    return solve_ranges(ranges, 202520252025)


app = AdventDay()
app.run()
