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


def load(filename):
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


def verify(data, instr):
    positive = [False for _ in instr[0]]
    negative = [False for _ in instr[0]]
    for plant in data.values():
        for branch in plant.branches:
            if branch.dest is None:
                assert branch.thickness == 1, "All input branches should have thickness 1"
                continue
            if branch.dest > len(instr[0]):
                assert branch.thickness > 0, f"Branch to {branch.dest} should have positive thickness"
                continue
            if branch.thickness < 0:
                negative[branch.dest-1] = True
            else:
                positive[branch.dest-1] = True
    test = all([a ^ b for a, b in zip(positive, negative)])
    assert test, "All inputs should contribute only positively or only negatively"
    return {i+1: (1 if a else 0) for i, a in enumerate(positive)}


# TODO: doesn't work for an example
def part3(data, last, instr):
    spell = verify(data, instr)
    max = traverse(data[last], data, spell)
    ducks = [traverse(data[last], data, i) for i in instr]
    ducks = [x for x in ducks if x > 0]
    return sum([max - x for x in ducks])


app = AdventDay()
app.run()
