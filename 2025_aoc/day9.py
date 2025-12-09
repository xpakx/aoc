from utils.loader import get_file
from utils.parser import parse
from utils.runner import AdventDay
from dataclasses import dataclass
from itertools import combinations


@dataclass
class Point:
    x: int
    y: int


def load(filename):
    data = get_file(filename)
    return parse(Point, "{x},{y}", data)


def get_area(p1, p2):
    return (abs(p1.x-p2.x)+1) * (abs(p1.y-p2.y)+1)


def task1(data):
    max = 0
    for p1, p2, in combinations(data, 2):
        area = get_area(p1, p2)
        if area > max:
            max = area
    return max


app = AdventDay()
app.run(test=False)
