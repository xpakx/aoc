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
    return [int(s) for s in re.findall(r'\d+', line)]


def load(filename):
    data = get_file(filename, split_by="\n\n")
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


def traverse(plant: Plant, plants: dict[int, Plant]):
    brightness = 0
    for branch in plant.branches:
        if branch.dest is None:
            brightness += 1
        else:
            brightness += branch.thickness*traverse(
                    plants.get(branch.dest), plants)
    if brightness < plant.thickness:
        return 0
    return brightness


def part1(data, last):
    return traverse(data[last], data)


app = AdventDay()
app.run()
