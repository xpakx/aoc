from utils.runner import AdventDay
from utils.loader import get_file


def load(filename):
    return get_file(filename, as_int=True, split_by=",")


def part1(nums):
    return sum([90 // x for x in nums])


app = AdventDay()
app.run()
