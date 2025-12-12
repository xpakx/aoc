from utils.loader import get_file
from utils.parser import parse
from utils.runner import AdventDay
from dataclasses import dataclass


@dataclass
class Box:
    id: int
    pattern: str

    def get_size(self):
        return self.pattern.count("#")


@dataclass
class Region:
    width: int
    height: int
    counts: list[int]

    def get_size(self):
        return self.width*self.height


def load(filename):
    data = get_file(filename, split_by="\n\n")
    boxes = [b.split(':') for b in data[:-1]]
    boxes = [Box(int(b[0]), b[1]) for b in boxes]
    regions = parse(Region, "{width}x{height}: {counts}", data[-1].split('\n'))
    return boxes, regions


def task1(boxes, regions):
    sizes = [b.get_size() for b in boxes]
    result = 0
    for region in regions:
        required = sum([c*b for c, b in zip(region.counts, sizes)])
        if required <= region.get_size():
            result += 1
    return result


app = AdventDay()
app.run(test=False)
