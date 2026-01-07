from utils.loader import get_file
from utils.runner import AdventDay
import heapq


def load1(filename):
    data = get_file(filename)
    stars = []
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell == '*':
                stars.append((i, j))
    return stars


def manhattan(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


def spanning_tree(stars, connections):
    queue = []
    visited = {star: False for star in stars}
    result = 0
    heapq.heappush(queue, (0, stars[0]))

    while queue:
        weight, node = heapq.heappop(queue)

        if visited[node]:
            continue

        result += weight
        visited[node] = True

        for edge in connections[node]:
            if not visited[edge[1]]:
                heapq.heappush(queue, (edge[0], edge[1]))

    return result


def task1(stars):
    connections = {star: [] for star in stars}
    for star in stars:
        for second in stars:
            if star == second:
                continue
            dist = manhattan(star, second)
            connections[star].append((dist, second))
    return spanning_tree(stars, connections) + len(stars)


app = AdventDay()
app.run()

