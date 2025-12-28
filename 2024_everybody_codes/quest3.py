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


def check_neighbors(cells, i, j, nums):
    for dir in dirs:
        i2 = i + dir[0]
        j2 = j + dir[1]
        if i2 < 0 or j2 < 0:
            continue
        if i2 >= len(cells) or j2 >= len(cells[i2]):
            continue
        if cells[i2][j2] != nums:
            return False
    return True


def step(data, num):
    cells = [row for row in data]
    to_increase = []
    for i, row in enumerate(cells):
        for j, cell in enumerate(row):
            if check_neighbors(cells, i, j, num):
                to_increase.append((i, j))
    for i, j in to_increase:
        cells[i][j] += 1
    return len(to_increase)


def task1(cells):
    i = 1
    while step(cells, i) > 0:
        i += 1
    result = 0
    for row in cells:
        for cell in row:
            result += cell
    return result


def task2(cells):
    return task1(cells)


app = AdventDay()
app.run()
