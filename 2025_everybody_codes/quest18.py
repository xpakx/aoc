from utils.runner import AdventDay
from utils.loader import get_file
from dataclasses import dataclass, field
import re


@dataclass
class Branch:
    dest: int | None = None
    source: int | None = None
    thickness: int = 0


@dataclass
class Plant:
    id: int
    thickness: int
    branches: list[int] = field(default_factory=list)


def get_all_ints(line):
    return [int(s) for s in re.findall(r'-?\d+', line)]

def get_plants(data):
    plants = {}
    have_connections = set()
    for plant in data:
        lines = plant.split('\n')
        branch_data = [get_all_ints(line) for line in lines[1:]]
        branch_data = [(b[0], b[1]) if len(b) > 1 else (None, b[0]) for b in branch_data]
        [id, thickness] = get_all_ints(lines[0])
        branches = []
        for (dest, bthickness) in branch_data:
            b = Branch(dest=dest, source=id, thickness=bthickness)
            branches.append(b)
            have_connections.add(dest)
        p = Plant(id, thickness, branches)
        plants[id] = p
    last = None
    for id in plants:
        if id not in have_connections:
            last = id
            break
    return plants, last


def load1(filename):
    data = get_file(filename, split_by="\n\n")
    return get_plants(data)


def load2(filename):
    data = get_file(filename, split_by="\n\n")
    plants, last = get_plants(data[:-1])
    instructions = []
    for instr in data[-1].split('\n'):
        inst = {i+1: num for i, num in enumerate(get_all_ints(instr))}
        instructions.append(inst)
    return plants, last, instructions


def traverse(plant: Plant, plants: dict[int, Plant], end=None):
    brightness = 0
    for branch in plant.branches:
        if branch.dest is None:
            if end is None or end[plant.id] == 1:
                brightness += branch.thickness
        else:
            brightness += branch.thickness*traverse(
                    plants.get(branch.dest), plants, end)
    if brightness < plant.thickness:
        return 0
    return brightness


def part1(data, last):
    return traverse(data[last], data)


def part2(data, last, instr):
    return sum([traverse(data[last], data, i) for i in instr])


app = AdventDay()
app.run()
