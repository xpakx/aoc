from utils.runner import AdventDay
from utils.loader import get_file
from collections import deque


def load(filename):
    data = get_file(filename, split_by=",")
    return [int(x[1:]) if x[0] == "R" else -int(x[1:]) for x in data]


def sign(value):
    if value < 0:
        return -1
    if value > 0:
        return 1
    return 0


def build_graph(data):
    graph = [(0, 0+sign(data[0]))]
    point = (0, 0)
    dir = (1, 0)
    for move in data:
        if move < 0:
            dir = (-dir[1], dir[0])
        else:
            dir = (dir[1], -dir[0])
        vec = (dir[0]*abs(move), dir[1]*abs(move))
        end = (point[0]-vec[0], point[1]-vec[1])
        graph.append(end)
        point = end
    end = graph.pop()
    graph.append((end[0]+dir[0], end[1]+dir[1]))
    return graph, end


def draw(graph, end):
    flat_x = [n[0] for n in graph]
    flat_y = [n[1] for n in graph]
    max_x = max(flat_x)
    min_x = min(flat_x)
    max_y = max(flat_y)
    min_y = min(flat_y)
    width = max_x-min_x+1
    height = max_y-min_y+1
    points = set()
    for i in range(len(graph)-1):
        p1 = graph[i]
        p2 = graph[i+1]
        if p1[0] == p2[0]:
            s = min(p1[1], p2[1])
            e = max(p1[1], p2[1])
            for j in range(s, e+1):
                points.add((p1[0], j))
        else:
            s = min(p1[0], p2[0])
            e = max(p1[0], p2[0])
            for j in range(s, e+1):
                points.add((j, p1[1]))
    for i in range(width):
        for j in range(height):
            point = (min_x+i, min_y+j)
            if point == (0, 0):
                print('S', end='')
            elif point == end:
                print('E', end='')
            elif point in points:
                print('#', end='')
            else:
                print('.', end='')
        print()


def build_grid(graph):
    flat_x = [n[0] for n in graph]
    flat_y = [n[1] for n in graph]
    max_x = max(flat_x)
    min_x = min(flat_x)
    max_y = max(flat_y)
    min_y = min(flat_y)
    width = max_x-min_x+1
    height = max_y-min_y+1
    points = set()
    for i in range(len(graph)-1):
        p1 = graph[i]
        p2 = graph[i+1]
        if p1[0] == p2[0]:
            s = min(p1[1], p2[1])
            e = max(p1[1], p2[1])
            for j in range(s, e+1):
                points.add((p1[0], j))
        else:
            s = min(p1[0], p2[0])
            e = max(p1[0], p2[0])
            for j in range(s, e+1):
                points.add((j, p1[1]))
    return width, height, points


dirs = [
        (0, 1), (1, 0), (0, -1), (-1, 0)
]


def shortest_path(points, start, end):
    queue = deque([(0, start)])
    visited = set(start)
    while queue:
        distance, node = queue.popleft()
        if node == end:
            return distance

        for dir in dirs:
            neighbor = (node[0]+dir[0], node[1]+dir[1])
            if neighbor in points:
                continue
            if neighbor in visited:
                continue
            visited.add(neighbor)
            queue.append((distance + 1, neighbor))
    return -1


def part1(data):
    graph, end = build_graph(data)
    w, h, grid = build_grid(graph)
    return shortest_path(grid, (0, 0), end)


def part2(data):
    return part1(data)


app = AdventDay()
app.run()
