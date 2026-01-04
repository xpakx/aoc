from utils.loader import get_file
from utils.runner import AdventDay
import heapq


def load(filename):
    data = get_file(filename)
    start = [(i, row.index('S')) for i, row in enumerate(data) if 'S' in row]
    return data, start[0]


def load3(filename):
    data = get_file(filename)
    start = [(i, row.index('E')) for i, row in enumerate(data) if 'E' in row]
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


def find_path(start, data, end='E'):
    queue = [(0, start)]
    heapq.heapify(queue)
    min_costs = {start: 0}
    while queue:
        cost, curr = heapq.heappop(queue)
        last = data[curr[0]][curr[1]]
        last_value = to_value(last)
        if last == end:
            return cost
        for neighbor in neighbors(curr, data):
            symbol = data[neighbor[0]][neighbor[1]]
            if symbol == '#':
                continue
            step_cost = abs(last_value - to_value(symbol))
            step_cost = min(step_cost, 10 - step_cost)
            new_cost = cost + step_cost + 1
            if new_cost < min_costs.get(neighbor, float('inf')):
                min_costs[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))


def task1(data, start):
    return find_path(start, data)


def task2(data, start):
    return find_path(start, data)


def task3(data, start):
    return find_path(start, data, 'S')


app = AdventDay()
app.run()
