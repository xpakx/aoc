from utils.loader import get_map
from utils.runner import AdventDay
from enum import Enum


class Tile(Enum):
    empty = 0
    paper = 1


def load(filename):
    return get_map(filename, Tile)


dirs = [
        [0, 1], [0, -1], [1, 1], [1, -1],
        [1, 0], [-1, 1], [-1, -1], [-1, 0]
]


def check_neighbour(map, pos, vec):
    x, y = pos
    vx, vy = vec
    x = x+vx
    y = y+vy
    if x < 0 or x >= len(map):
        return False
    line = map[x]
    if y < 0 or y >= len(line):
        return False
    return map[x][y] == Tile.paper


def task1(map):
    result = 0
    for i, line in enumerate(map):
        for j, elem in enumerate(line):
            if elem == Tile.paper:
                neighbours = [
                        check_neighbour(map, [i, j], dir) for dir in dirs
                ].count(True)
                if neighbours < 4:
                    result += 1
    return result


app = AdventDay()
app.run()
