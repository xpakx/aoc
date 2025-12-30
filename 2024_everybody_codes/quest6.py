from utils.loader import get_file
from utils.runner import AdventDay
from collections import Counter, deque


def load(filename):
    data = get_file(filename)
    graph = {}
    for line in data:
        node_in, out = line.split(':', maxsplit=1)
        out = out.split(',')
        graph[node_in] = out
    return graph


def task1(graph):
    nodes = [('RR', 0, 'RR')]
    fruits = {}
    fruit_paths = {}
    while nodes:
        fruit, path_len, path = nodes.pop()
        next = graph.get(fruit)
        if next is None:
            continue
        if '@' in next:
            fruits[fruit] = path_len+1
            fruit_paths[fruit] = path + '@'
        new = [(n, path_len+1, path + n) for n in next if n != '@']
        nodes.extend(new)
    value_counts = Counter(fruits.values())
    for fruit, val in fruits.items():
        if value_counts[val] == 1:
            return fruit_paths[fruit]


def task2(graph):
    nodes = [('RR', 0, 'R')]
    fruits = {}
    fruit_paths = {}
    while nodes:
        fruit, path_len, path = nodes.pop()
        next = graph.get(fruit)
        if next is None:
            continue
        if '@' in next:
            fruits[fruit] = path_len+1
            fruit_paths[fruit] = path + '@'
        new = [(n, path_len+1, path + n[0]) for n in next if n != '@']
        nodes.extend(new)
    value_counts = Counter(fruits.values())
    for fruit, val in fruits.items():
        if value_counts[val] == 1:
            return fruit_paths[fruit]


def task3(graph):
    nodes = [('RR', 0, set('RR'), 'R')]
    fruits = {}
    while nodes:
        fruit, path_len, visited, path = nodes.pop()
        if fruit == '@':
            fruits[path] = path_len
            continue
        visited.add(fruit)
        next = graph.get(fruit)
        if next is None:
            continue
        new = [(n, path_len+1, set(visited), path + n[0]) for n in next if n not in visited]
        nodes.extend(new)
    value_counts = Counter(fruits.values())
    for fruit, val in fruits.items():
        if value_counts[val] == 1:
            return fruit


app = AdventDay()


@app.task(part=3)
def task3_bfs(graph):
    queue = deque([('RR', 0, {'RR'}, 'R')])
    while queue:
        level_fruits = {}
        for _ in range(len(queue)):
            curr, dist, visited, path = queue.popleft()
            neighbors = graph.get(curr, [])
            if not neighbors:
                continue
            for n in neighbors:
                if n == '@':
                    level_fruits[path + '@'] = dist + 1
                elif n not in visited:
                    new_visited = visited | {n}
                    queue.append((n, dist + 1, new_visited, path + n[0]))
        if level_fruits:
            if len(level_fruits) == 1:
                return list(level_fruits.keys())[0]


app.run()
