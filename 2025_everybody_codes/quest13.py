from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename, as_int=True)


def part1(nums):
    base = len(nums) + 1
    print(base)
    curr = 2025 % base
    reshaped = [1] + nums[::2] + nums[1::2][::-1]
    print(nums)
    print(reshaped)
    return reshaped[curr]


app = AdventDay()
app.run()
