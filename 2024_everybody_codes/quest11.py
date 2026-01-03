from utils.loader import get_file
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass


@dataclass
class Termite:
    id: str
    conversions: list[str]


def load(filename):
    data = get_file(filename)
    parsed = parse(Termite, "{id}:{conversions}", data, list_separator=',')
    return {x.id: x for x in parsed}


def convert(map, start, steps):
    counts = {start: 1}
    for _ in range(steps):
        new_counts = {}
        for termite, count in counts.items():
            curr = map.get(termite)
            for t in curr.conversions:
                new_counts.setdefault(t, 0)
                new_counts[t] += count
        counts = new_counts
    return sum(counts.values())


def task1(data):
    return convert(data, 'A', 4)


def task2(data):
    return convert(data, 'Z', 10)


def task3(data):
    results = [convert(data, x, 20) for x in data.keys()]
    return max(results) - min(results)


app = AdventDay()
app.run()
