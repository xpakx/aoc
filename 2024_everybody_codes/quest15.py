from utils.loader import get_file
from utils.runner import AdventDay
import heapq
from collections import deque


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
    k = (1 << len(herbs)) - 1
    queue = deque([(0, start, 0)])
    visited = {(start, 0)}
    while queue:
        cost, curr, found_herbs = queue.popleft()
        if curr == start and found_herbs == k:
            return cost
        for neighbor in neighbors(curr):
            if neighbor[0] < 0:
                continue
            symbol = data[neighbor[0]][neighbor[1]]
            if symbol == '#':
                continue
            if symbol == '~':
                continue
            val = ord(symbol) - 65
            new_herbs = found_herbs
            if 0 <= val < len(herbs):
                new_herbs = new_herbs | (1 << val)
            if (neighbor, new_herbs) in visited:
                continue
            visited.add((neighbor, new_herbs))
            queue.append((cost+1, neighbor, new_herbs))


def task2(data, start):
    herbs = set()
    for row in data:
        for cell in row:
            if cell not in ['#', '~', '.']:
                herbs.add(cell)
    return find_path2(start, data, herbs)


app = AdventDay()
app.run()
