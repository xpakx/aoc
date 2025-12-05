from utils.loader import get_map
from utils.runner import AdventDay
from enum import Enum


class Tile(Enum):
    empty = 0
    sheep = 1
    dragon = 2


def load(filename):
    map = get_map(filename, Tile, dct={'S': Tile.sheep, 'D': Tile.dragon})
    dragon_row = next(
            filter(lambda x: Tile.dragon in x[1], enumerate(map))
    )
    dragon_tile = next(
            filter(lambda x: Tile.dragon == x[1], enumerate(dragon_row[1]))
    )

    print(dragon_row, dragon_tile)
    return map, [dragon_row[0], dragon_tile[0]]


moves = [
        [2, 1], [2, -1], [-2, 1], [-2, -1],
        [1, 2], [1, -2], [-1, 2], [-1, -2]
]


def part1(map, dragon_pos):
    stack = [[*dragon_pos, 0]]
    visited = [[False for tile in row] for row in map]
    result = 0
    max_steps = 4
    while len(stack) > 0:
        [i, j, steps] = stack.pop()
        if steps > max_steps:
            continue
        for m in moves:
            new_i = i + m[0]
            new_j = j + m[1]
            if new_i < 0 or new_j < 0:
                continue
            if new_i >= len(map) or new_j >= len(map[new_i]):
                continue
            stack.append([new_i, new_j, steps+1])
        if visited[i][j]:
            continue
        visited[i][j] = True
        if map[i][j] == Tile.sheep:
            result += 1
    for row in visited:
        for cell in row:
            if cell:
                print("x", end="")
            else:
                print(".", end="")
        print()
    return result


app = AdventDay()
app.run(test=False)
