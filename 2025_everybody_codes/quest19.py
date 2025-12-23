from utils.runner import AdventDay
from utils.loader import get_file
from utils.parser import parse
from dataclasses import dataclass
import heapq
from collections import defaultdict
from math import ceil


@dataclass
class Column:
    position: int
    height: int
    gap: int

    def in_gap(self, height):
        return height >= self.height and height < self.height + self.gap


def load(filename):
    data = get_file(filename)
    return parse(Column, "{position},{height},{gap}", data)


moves = [-1, 1]


def in_gap(height, columns):
    return any([col.in_gap(height) for col in columns])


def shortest_path(columns: list[Column]):
    heap = [(0, 0, 0)]
    goal = columns[-1].position
    column_map = defaultdict(list)
    for col in columns:
        column_map[col.position].append(col)
    visited = set()
    while heap:
        flaps, position, height = heapq.heappop(heap)
        if position == goal:
            return flaps

        for move in moves:
            new_pos = position + 1
            new_height = height + move
            if (new_pos, new_height) in visited:
                continue
            visited.add((new_pos, new_height))
            columns = column_map.get(new_pos)
            if columns and not in_gap(new_height, columns):
                continue
            cost = flaps + ((move + 1) // 2)
            heapq.heappush(heap, (cost, new_pos, new_height))
    return -1


def part1(data):
    return shortest_path(data)


def part2(data):
    return shortest_path(data)


# TODO: that doesn't work for every input and assumes
# lots of things
def part3(data):
    max_xy = 0
    furthest_x = 0
    for column in data:
        if column.position > furthest_x:
            furthest_x = column.position
            max_xy = max(column.position + column.height, max_xy)
    return ceil(max_xy / 2)


app = AdventDay()
app.run()
