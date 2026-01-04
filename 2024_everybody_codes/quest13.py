from utils.loader import get_file
from utils.runner import AdventDay
from collections import deque
import heapq


def load(filename):
    data = get_file(filename)
    start = [(i, row.index('S')) for i, row in enumerate(data) if 'S' in row]
    return data, start[0]


dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def neighbors(elem, data):
    all = [(elem[0]+i, elem[1]+j) for i, j in dirs]
    return [(i, j) for i, j in all
            if i >= 0 and j >= 0 and i < len(data) and j < len(data[i])
            ]


def to_value(symbol):
    if symbol in ['S', 'E']:
        return 0
    return ord(symbol)-48


def find_path(start, data):
    queue = [(0, start)]
    heapq.heapify(queue)
    min_costs = {start: 0}
    while queue:
        cost, curr = heapq.heappop(queue)
        last = data[curr[0]][curr[1]]
        last_value = to_value(last)
        if last == 'E':
            return cost
        for neighbor in neighbors(curr, data):
            symbol = data[neighbor[0]][neighbor[1]]
            if symbol == '#':
                continue
            step_cost = abs(last_value - to_value(symbol))
            new_cost = cost + step_cost + 1
            if new_cost < min_costs.get(neighbor, float('inf')):
                min_costs[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))


def task1(data, start):
    print(data)
    print(start)
    return find_path(start, data)


app = AdventDay()
app.run()
