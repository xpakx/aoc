from utils.runner import AdventDay
from utils.loader import get_file
import math


def load(filename):
    return get_file(filename, as_int=True, split_by=",")


def part1(nums):
    return sum([90 // x for x in nums])


class Sieve:
    def __init__(self, len):
        self.sieve = [0] * len

    def use(self, number):
        n = 1
        while n * number <= len(self.sieve):
            self.sieve[n*number-1] += 1
            n += 1

    def check(self, number):
        return self.sieve[number-1] == 0

    def get(self, number):
        return self.sieve[number-1]


def part2(nums):
    result = []
    sieve = Sieve(len(nums))
    for i, val in enumerate(nums):
        num = i+1
        v = val - sieve.get(num)
        if v > 0:
            result.append(num)
            sieve.use(num)
    return math.prod(result)


app = AdventDay()
app.run()
