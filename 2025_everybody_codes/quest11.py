from utils.loader import get_file
from utils.runner import AdventDay
from enum import Enum


class Tile(Enum):
    empty = 0
    sheep = 1
    dragon = 2
    wall = 3


def load(filename):
    return get_file(filename, as_int=True)


def step(nums):
    moved = False
    for i in range(len(nums)-1):
        if nums[i] > nums[i+1]:
            nums[i] -= 1
            nums[i+1] += 1
            moved = True
    return moved


def step_second_phase(nums):
    moved = False
    for i in range(len(nums)-1):
        if nums[i] < nums[i+1]:
            nums[i+1] -= 1
            nums[i] += 1
            moved = True
    return moved


def checksum(nums):
    return sum([x*(i+1) for i, x in enumerate(nums)])


def part1(nums):
    print("0:", nums)
    phase = 1
    for i in range(10):
        if phase == 1:
            moved = step(nums)
        if not moved:
            phase = 2
        if phase == 2:
            moved = step_second_phase(nums)
        if not moved:
            break
        print(f"{i+1}: {nums}")

    print(nums)
    return checksum(nums)


def part2(nums):
    phase = 1
    i = 0
    balanced = False
    while not balanced:
        if phase == 1:
            moved = step(nums)
        if not moved:
            phase = 2
        if phase == 2:
            moved = step_second_phase(nums)
        if not moved:
            break
        i += 1

    return i


app = AdventDay()
app.run()
