from utils.loader import get_file
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


def load(filename) -> list[Point]:
    return parse(Point, "x={x} y={y}", get_file(filename))


def coord_to_disk(x, y) -> int:
    return x - 1


def disk_to_coord(pos, disk) -> Point:
    return Point(pos + 1, disk - pos)


def task1(data: list[Point]):
    days = 100
    result = 0
    for snail in data:
        disc = snail.x + snail.y - 1
        p = coord_to_disk(snail.x, snail.y)
        p = (p+days) % disc
        pos = disk_to_coord(p, disc)
        result += pos.x + 100*pos.y
    return result


app = AdventDay()
app.run()
