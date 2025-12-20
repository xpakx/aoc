from utils.runner import AdventDay
from utils.loader import get_map
from enum import Enum


class Tile(Enum):
    inactive = 0
    active = 1


def load(filename):
    return get_map(filename, Tile, dct={'.': Tile.inactive, "#": Tile.active})


dirs = [
        (-1, -1), (1, 1), (1, -1), (-1, 1)
]


def check_neighbours(old, next):
    for i in range(len(old)):
        for j in range(len(old[i])):
            n = 0
            for dir in dirs:
                i2 = i+dir[0]
                j2 = j+dir[1]
                if i2 < 0 or i2 >= len(old):
                    continue
                if j2 < 0 or j2 >= len(old[i]):
                    continue
                if old[i2][j2]:
                    n += 1
            if old[i][j]:
                next[i][j] = n % 2 == 1
            else:
                next[i][j] = n % 2 == 0


def clean_table(tbl):
    for i in range(len(tbl)):
        for j in range(len(tbl[i])):
            tbl[i][j] = False


def count(tbl):
    result = 0
    for i in range(len(tbl)):
        for j in range(len(tbl[i])):
            if tbl[i][j]:
                result += 1
    return result


def part1(floor):
    print(floor)
    old = [[tile == Tile.active for tile in row] for row in floor]
    next = [[False for tile in row] for row in floor]
    result = 0
    for i in range(10):
        check_neighbours(old, next)
        result += count(next)
        print(count(next))
        old, next = next, old
        clean_table(next)
    print(next)
    print(result)
    return result


def part2(floor):
    old = [[tile == Tile.active for tile in row] for row in floor]
    next = [[False for tile in row] for row in floor]
    result = 0
    for i in range(2025):
        check_neighbours(old, next)
        result += count(next)
        old, next = next, old
        clean_table(next)
    return result


app = AdventDay()
app.run()
