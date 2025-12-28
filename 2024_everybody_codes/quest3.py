from utils.loader import get_map
from utils.runner import AdventDay
from enum import Enum


class Cell(Enum):
    empty = 0
    block = 1


def load(filename):
    data = get_map(filename, Cell, dct={'#': Cell.block})
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell == Cell.empty:
                data[i][j] = 0
            else:
                data[i][j] = 1
    return data


dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
dirs_diag = dirs + [(-1, 1), (1, 1), (1, -1), (-1, -1)]


def check_neighbors(cells, i, j, nums, dirs):
    for dir in dirs:
        i2 = i + dir[0]
        j2 = j + dir[1]
        if i2 < 0 or j2 < 0:
            return False
        if i2 >= len(cells) or j2 >= len(cells[i2]):
            return False
        if cells[i2][j2] != nums:
            return False
    return True


def step(data, num, dirs=dirs):
    cells = [row for row in data]
    to_increase = []
    for i, row in enumerate(cells):
        for j, cell in enumerate(row):
            if cell == 0:
                continue
            if check_neighbors(cells, i, j, num, dirs):
                to_increase.append((i, j))
    for i, j in to_increase:
        cells[i][j] += 1
    return len(to_increase)


def count(cells):
    result = 0
    for row in cells:
        for cell in row:
            result += cell
    return result


def draw(cells):
    for row in cells:
        for cell in row:
            if cell == 0:
                print('.', end='')
            else:
                print(cell, end='')
        print()


def task1(cells):
    i = 1
    while step(cells, i) > 0:
        i += 1
    return count(cells)


def task2(cells):
    return task1(cells)


def task3(cells):
    i = 1
    while step(cells, i, dirs=dirs_diag) > 0:
        i += 1
    # draw(cells)
    return count(cells)


app = AdventDay()
app.run()
