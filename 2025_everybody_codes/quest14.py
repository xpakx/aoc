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


def solve_lists(floor, steps):
    old = [[tile == Tile.active for tile in row] for row in floor]
    next = [[False for tile in row] for row in floor]
    result = 0
    for i in range(steps):
        check_neighbours(old, next)
        result += count(next)
        old, next = next, old
        clean_table(next)
    return result


def print_bin(num):
    print(''.join(reversed(format(num, '#036b')[2:])))


def check_neighbours_bin(old, new, width_mask):
    for i, row in enumerate(old[1:-1]):
        curr = i + 1
        prev = (old[curr-1] << 1) ^ (old[curr-1] >> 1)
        next = (old[curr+1] << 1) ^ (old[curr+1] >> 1)
        mask = prev ^ next
        new[curr] = ~(mask ^ row) & width_mask


def clean_table_bin(tbl):
    for i in range(len(tbl)):
        tbl[i] = 0


def count_bin(tbl):
    result = 0
    for row in tbl:
        result += row.bit_count()
    return result


def solve_bitmask(floor, steps):
    rows = []
    for row in floor:
        mask = 0
        shift = 0
        for tile in row:
            if tile == Tile.active:
                mask |= (1 << shift)
            shift += 1
        rows.append(mask)
    rows = [0] + rows + [0]
    next = [0 for row in floor]
    next = [0] + next + [0]
    result = 0
    width_mask = (1 << len(floor[0])) - 1
    for i in range(steps):
        check_neighbours_bin(rows, next, width_mask)
        result += count_bin(next)
        rows, next = next, rows
        clean_table_bin(next)
    return result


def part1(floor):
    return solve_bitmask(floor, 10)


def part2(floor):
    return solve_bitmask(floor, 2025)


app = AdventDay()


@app.task(1)
def part1_lists(floor):
    return solve_lists(floor, 10)


@app.task(2)
def part2_lists(floor):
    return solve_lists(floor, 2025)


app.run()
