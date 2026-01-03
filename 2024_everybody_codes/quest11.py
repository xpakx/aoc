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
    return parse(Termite, "{id}:{conversions}", data, list_separator=',')


def task1(data):
    map = {x.id: x for x in data}
    current = ['A']
    for _ in range(4):
        new_current = []
        for termite in current:
            curr = map.get(termite)
            new_current.extend(curr.conversions)
        current = new_current
    return len(current)


app = AdventDay()
app.run()
