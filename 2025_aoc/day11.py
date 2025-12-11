from utils.loader import get_file
from utils.parser import parse
from utils.runner import AdventDay
from dataclasses import dataclass


@dataclass
class Connection:
    id: str
    nodes: list[str]


def load(filename):
    data = get_file(filename)
    return parse(Connection, "{id}: {nodes}", data)


def all_paths(start: str, end: str, conns) -> int:
    queue = [start]
    result = 0
    while queue:
        elem = queue.pop()
        if elem == end:
            result += 1
            continue
        conn = conns.get(elem)
        if not conn:
            continue
        queue.extend(conn.nodes)
    return result


def task1(data):
    conns = {conn.id: conn for conn in data}
    return all_paths("you", "out", conns)


app = AdventDay()
app.run(test=False)
