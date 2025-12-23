from utils.loader import get_map
from utils.runner import AdventDay
from enum import Enum
import heapq
from math import ceil


class Tile(Enum):
    empty = 0
    wall = 1
    trampoline = 2
    start = 3
    end = 4


def load(filename):
    return get_map(filename, Tile,
                   dct={
                       'T': Tile.trampoline,
                       'S': Tile.start,
                       'E': Tile.end,
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


def shortest_path(maze, start, goal):
    heap = [(0, start[0], start[1])]
    visited = set()
    while heap:
        cost, i, j = heapq.heappop(heap)
        position = (i, j)
        if position == goal:
            return cost

        for new_pos in get_neighbors(i, j):
            if new_pos in visited:
                continue
            if not trampoline_at(new_pos[0], new_pos[1], maze):
                continue
            visited.add(new_pos)
            heapq.heappush(heap, (cost+1, new_pos[0], new_pos[1]))
    return -1


def part2(maze):
    goal = (0, 0)
    start = (0, 0)
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == Tile.start:
                start = (i, j)
            if cell == Tile.end:
                goal = (i, j)
                maze[i][j] = Tile.trampoline
    return shortest_path(maze, start, goal)


# based on barycentric coordinates, but adjusted for 'skewedness'
def rotate(i, j, maze):
    j = j-i  # unskewing
    new_i = (len(maze) - 1) - i - ceil(j/2)
    new_j = 2*i if j % 2 == 0 else 2 * i + 1
    new_j = new_j + new_i  # reskewing
    return (new_i, new_j)


def shortest_path_with_rotation(maze, start, goal):
    heap = [(0, start[0], start[1])]
    visited = set()
    while heap:
        cost, i, j = heapq.heappop(heap)
        position = (i, j)
        if position == goal:
            return cost

        i, j = rotate(i, j, maze)
        neighbors = get_neighbors(i, j) + [(i, j)]

        for new_pos in neighbors:
            if new_pos in visited:
                continue
            if not trampoline_at(new_pos[0], new_pos[1], maze):
                continue
            visited.add(new_pos)
            heapq.heappush(heap, (cost+1, new_pos[0], new_pos[1]))
    return -1


def part3(maze):
    goal = (0, 0)
    start = (0, 0)
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == Tile.start:
                start = (i, j)
            if cell == Tile.end:
                goal = (i, j)
                maze[i][j] = Tile.trampoline
    return shortest_path_with_rotation(maze, start, goal)


app = AdventDay()
app.run()
