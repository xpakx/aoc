from utils.loader import get_file
from utils.runner import AdventDay
from collections import deque


def load(filename):
    data = get_file(filename)
    start = [(i, row.index('S')) for i, row in enumerate(data) if 'S' in row]
    return data, start[0]


dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def neighbors(elem):
    return [(elem[0]+i, elem[1]+j) for i, j in dirs]


def find_path(start, data):
    # alt, steps, pos, prev
    queue = deque([(1000, 0, start, None)])
    visited = {(0, start, None)}
    max_alt = 0
    while queue:
        altitude, steps, curr, prev = queue.popleft()
        if steps == 100:
            if altitude > max_alt:
                max_alt = altitude
            continue
        for neighbor in neighbors(curr):
            if neighbor[0] < 0 or neighbor[1] < 0:
                continue
            if neighbor[0] >= len(data) or neighbor[1] >= len(data[0]):
                continue
            if neighbor == prev:
                continue
            symbol = data[neighbor[0]][neighbor[1]]
            if symbol == '#':
                continue
            new_alt = altitude
            if symbol == '-':
                new_alt -= 2
            elif symbol == '+':
                new_alt += 1
            else:
                new_alt -= 1
            if (new_alt, neighbor, curr) in visited:
                continue
            if new_alt < 0:
                continue
            visited.add((new_alt, neighbor, curr))
            queue.append((new_alt, steps+1, neighbor, curr))
    return max_alt


def part1(data, start):
    return find_path(start, data)


app = AdventDay()
app.run()
