from utils.runner import AdventDay
from utils.loader import get_file
from utils.parser import parse
from dataclasses import dataclass
import heapq


@dataclass
class Column:
    position: int
    height: int
    gap: int


def load(filename):
    data = get_file(filename)
    return parse(Column, "{position},{height},{gap}", data)


moves = [-1, 1]


def in_gap(height, column):
    return height >= column.height and height < column.height + column.gap


def shortest_path(columns: list[Column]):
    heap = [(0, 0, 0)]
    goal = columns[-1].position
    column_map = {col.position: col for col in columns}
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
            if new_height < 0 or new_height > 40:
                continue
            column = column_map.get(new_pos)
            if column and not in_gap(new_height, column):
                continue
            cost = flaps + ((move + 1) // 2)
            heapq.heappush(heap, (cost, new_pos, new_height))
    return -1


def part1(data):
    return shortest_path(data)


app = AdventDay()
app.run()
