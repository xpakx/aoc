from utils.loader import get_file
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass
from math import lcm


@dataclass
class Snail:
    x: int
    y: int
    disc: int = 0
    offset: int = 0


def load(filename) -> list[Snail]:
    return parse(Snail, "x={x} y={y}", get_file(filename))


def coord_to_disk(x, y) -> int:
    return x - 1


def disk_to_coord(pos, disk) -> Snail:
    return Snail(pos + 1, disk - pos)


def task1(data: list[Snail]):
    days = 100
    result = 0
    for snail in data:
        disc = snail.x + snail.y - 1
        p = coord_to_disk(snail.x, snail.y)
        p = (p+days) % disc
        pos = disk_to_coord(p, disc)
        result += pos.x + 100*pos.y
    print(data)


def task2(data: list[Snail]):
    days = 0
    total_size = 1
    for snail in data:
        snail.disc = snail.x + snail.y - 1
        snail.offset = snail.disc - snail.x
        while (days - snail.offset) % snail.disc != 0:
            days += total_size
        total_size = lcm(snail.disc, total_size)
    return days


def task3(data: list[Snail]):
    return task2(data)


app = AdventDay()
app.run()
