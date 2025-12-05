from utils.loader import get_file_instr
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int


def load(filename):
    [ranges, nums] = get_file_instr(filename, split_first_by='\n', split_second_by='\n')
    nums = [int(n) for n in nums]
    ranges = parse(Range, "{start}-{end}", ranges)
    ranges.sort(key=lambda x: x.start)
    return ranges, nums


def join_ranges(ranges):
    result = [ranges[0]]
    for r in ranges[1:]:
        last = result[-1]
        if r.start <= last.end:
            last.end = max(last.end, r.end)
        else:
            result.append(r)
    return result


def task1(ranges, numbers):
    ranges = join_ranges(ranges)
    result = 0
    for n in numbers:
        fresh = False
        for r in ranges:
            if n >= r.start and n <= r.end:
                fresh = True
                break
            if n < r.start:
                break
        if fresh:
            result += 1
    return result


app = AdventDay()
app.run(test=False)
