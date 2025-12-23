from utils.loader import get_map
from utils.runner import AdventDay
from enum import Enum


class Tile(Enum):
    empty = 0
    wall = 1
    trampoline = 2


def load(filename):
    return get_map(filename, Tile,
                   dct={
                       'T': Tile.trampoline,
                       '#': Tile.wall,
                       }
                   )


def trampoline_at(i, j, maze):
    if i < 0 or j < 0:
        return False
    if i >= len(maze) or j >= len(maze[i]):
        return False
    return maze[i][j] == Tile.trampoline


def get_neighbors(i, j):
    return [
            (i, j-1),
            (i, j+1),
            (i-1, j) if i % 2 == j % 2 else (i+1, j)
            ]


def part1(maze):
    result = 0
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell != Tile.trampoline:
                continue
            for x, y in get_neighbors(i, j):
                if trampoline_at(x, y, maze):
                    result += 1
    return result // 2


app = AdventDay()
app.run()
