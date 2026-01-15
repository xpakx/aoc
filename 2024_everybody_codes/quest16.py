from utils.loader import get_file
from utils.runner import AdventDay
from collections import Counter
from math import lcm
from functools import cache


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


def count(wheels, nums, steps):
    curr = [0] * len(nums)
    r = []
    for _ in range(steps):
        for i, _ in enumerate(curr):
            mod = len(wheels[i])
            change = nums[i]
            curr[i] = (curr[i] + change) % mod
        eyes = [wheels[i][x][0]+wheels[i][x][2] for i, x in enumerate(curr)]
        result = ''.join(eyes)
        counts = Counter(result)
        coins = 0
        for value in counts.values():
            if value >= 3:
                coins += value - 2
        r.append(coins)
    return r


def task2(wheels, nums):
    cycle = 1
    for wheel in wheels:
        cycle = lcm(len(wheel), cycle)
    print(cycle)
    steps = 202420242024
    quotient = steps // cycle
    remainder = steps % cycle
    coins = count(wheels, nums, cycle)

    first = sum([coins[i] for i in range(0, remainder)])
    second = sum([coins[i] for i in range(remainder, cycle)])
    return first + quotient * (first + second)


@cache
def find_max_min(
        wheels, nums, total, wheel_offset=0, pull_number=0
):
    line = ""
    for dist, wheel in zip(nums, wheels):
        pos = (pull_number*dist+wheel_offset) % len(wheel)
        line += wheel[pos][0] + wheel[pos][2]
    score = 0
    if pull_number > 0:
        score = sum(i-2 for i in Counter(line).values() if i > 2)
    if total - pull_number > 0:
        curr_max = 0
        curr_min = float('inf')
        for i in (-1, 0, 1):
            r_max, r_min = find_max_min(
                    wheels, nums, total,
                    wheel_offset+i, pull_number+1)
            if r_max > curr_max:
                curr_max = r_max
            if r_min < curr_min:
                curr_min = r_min

        return score + curr_max, score + curr_min
    return score, score


def task3(wheels, nums):
    wheels = tuple([tuple(x) for x in wheels])
    print(wheels)
    print(nums)
    max, min = find_max_min(wheels, tuple(nums), 256)
    return f"{max} {min}"


app = AdventDay()
app.run()
