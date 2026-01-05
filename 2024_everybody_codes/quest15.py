from utils.loader import get_file
from utils.runner import AdventDay
import heapq


def load(filename):
    data = get_file(filename)
    start = data[0].index('.')
    return data, (0, start)


dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def neighbors(elem):
    return [(elem[0]+i, elem[1]+j) for i, j in dirs]


def find_path(start, data):
    queue = [(0, start)]
    heapq.heapify(queue)
    min_costs = {start: 0}
    while queue:
        cost, curr = heapq.heappop(queue)
        if data[curr[0]][curr[1]] == 'H':
            return cost
        for neighbor in neighbors(curr):
            symbol = data[neighbor[0]][neighbor[1]]
            if symbol == '#':
                continue
            if neighbor == start:
                continue
            if cost + 1 < min_costs.get(neighbor, float('inf')):
                min_costs[neighbor] = cost + 1
                heapq.heappush(queue, (cost+1, neighbor))


def task1(data, start):
    return 2*find_path(start, data)


def find_path2(start, data, herbs):
    k = tuple([False]*len(herbs))
    queue = [(0, start, k)]
    heapq.heapify(queue)
    min_costs = {(start, k): 0}
    while queue:
        cost, curr, found_herbs = heapq.heappop(queue)
        if curr == start and all(found_herbs):
            return cost
        for neighbor in neighbors(curr):
            symbol = data[neighbor[0]][neighbor[1]]
            if symbol == '#':
                continue
            if symbol == '~':
                continue
            if neighbor[0] < 0:
                continue
            val = ord(symbol) - 65
            new_herbs = tuple([True if i == val else x for i, x in enumerate(found_herbs)])
            if cost + 1 < min_costs.get((neighbor, new_herbs), float('inf')):
                min_costs[(neighbor, new_herbs)] = cost + 1
                heapq.heappush(queue, (cost+1, neighbor, new_herbs))


def task2(data, start):
    herbs = set()
    for row in data:
        for cell in row:
            if cell not in ['#', '~', '.']:
                herbs.add(cell)
    return find_path2(start, data, herbs)


app = AdventDay()
app.run()
