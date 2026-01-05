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
    print(data)
    print(start)
    return 2*find_path(start, data)


app = AdventDay()
app.run()
