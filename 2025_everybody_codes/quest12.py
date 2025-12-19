from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return [list(x) for x in get_file(filename)]


dirs = [
        (0, 1), (1, 0), (0, -1), (-1, 0)
]


class Vec2(tuple):
    def __new__(cls, x, y):
        return super().__new__(cls, (x, y))

    def __add__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            return Vec2(self[0] + other[0], self[1] + other[1])
        return super().__add__(other)

    def __radd__(self, other):
        if other == 0:
            return self
        return self.__add__(other)

    def valid(self, width, height) -> bool:
        if self[0] < 0 or self[1] < 0:
            return False
        if self[0] >= height or self[1] >= width:
            return False
        return True

    def neighbors(self, width, height, test=None) -> list["Vec2"]:
        result = []
        for dir in dirs:
            n = self + dir
            if not n.valid(width, height):
                continue
            if test and not test(n):
                continue
            result.append(n)
        return result


def print_map(nums, visited):
    for x, row in enumerate(nums):
        for y, cell in enumerate(row):
            if (x, y) in visited:
                print("*", end="")
            else:
                print(cell, end="")
        print()


def part1(nums):
    queue = [Vec2(0, 0)]
    visited = set()
    result = 0
    while len(queue) > 0:
        pos = queue.pop()
        if pos in visited:
            continue
        visited.add(pos)

        result += 1
        neighbors = pos.neighbors(
                len(nums[0]), len(nums),
                lambda x: nums[x[0]][x[1]] <= nums[pos[0]][pos[1]]
        )
        queue.extend(neighbors)

    return result


def part2(nums):
    queue = [Vec2(0, 0), Vec2(len(nums)-1, len(nums[0])-1)]
    visited = set()
    # print_map(nums, queue)
    result = 0
    while len(queue) > 0:
        pos = queue.pop()
        if pos in visited:
            continue
        visited.add(pos)

        result += 1
        neighbors = pos.neighbors(
                len(nums[0]), len(nums),
                lambda x: nums[x[0]][x[1]] <= nums[pos[0]][pos[1]]
        )
        queue.extend(neighbors)

    return result


app = AdventDay()
app.run()
