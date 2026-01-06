from utils.loader import get_file
from utils.runner import AdventDay
from collections import Counter
from math import lcm


def load(filename):
    data = get_file(filename, split_by='\n\n')
    nums = [int(x) for x in data[0].split(',')]
    data = data[1].split('\n')
    wheels_len = (len(data[0]) + 1) // 4
    wheels = [[] for x in range(wheels_len)]
    for row in data:
        for i in range(0, len(row), 4):
            if row[i] == ' ':
                continue
            wheels[i//4].append(row[i:i+3])
    return wheels, nums


def task1(wheels, nums):
    curr = [0] * len(nums)
    for _ in range(100):
        for i, _ in enumerate(curr):
            mod = len(wheels[i])
            change = nums[i]
            curr[i] = (curr[i] + change) % mod
    print(curr)
    result = [wheels[i][x] for i, x in enumerate(curr)]
    return " ".join(result)


def task2(wheels, nums):
    cycle = 1
    for wheel in wheels:
        cycle = lcm(len(wheel), cycle)
    print(cycle)
    steps = 202420242024
    quotient = steps // cycle
    remainder = steps % cycle
    print(quotient, remainder)


app = AdventDay()
app.run()
