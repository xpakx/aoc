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
    # return all_paths("you", "out", conns)
    return all_paths_recur("you", "out", conns, {})


def all_paths_recur(current: str, end: str, conns, visited) -> int:
    if current in visited:
        return visited[current]

    if current == end:
        return 1

    paths = 0
    conn = conns.get(current)
    if not conn:
        return 0
    for c in conn.nodes:
        paths += all_paths_recur(c, end, conns, visited)

    visited[current] = paths
    return paths


def task2(data):
    conns = {conn.id: conn for conn in data}
    svr_to_dac = all_paths_recur('svr', 'dac', conns, {})
    dac_to_fft = all_paths_recur('dac', 'fft', conns, {})
    fft_to_out = all_paths_recur('fft', 'out', conns, {})
    option1 = svr_to_dac*dac_to_fft*fft_to_out

    svr_to_fft = all_paths_recur('svr', 'fft', conns, {})
    fft_to_dac = all_paths_recur('fft', 'dac', conns, {})
    dac_to_out = all_paths_recur('dac', 'out', conns, {})
    option2 = svr_to_fft*fft_to_dac*dac_to_out 
    return option1 + option2


app = AdventDay()
app.run(test=False)
