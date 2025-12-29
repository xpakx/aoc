from utils.loader import get_file
from utils.runner import AdventDay
from collections import Counter


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




app = AdventDay()
app.run()
