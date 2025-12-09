from utils.loader import get_file
from utils.parser import parse
from utils.runner import AdventDay
from dataclasses import dataclass
from itertools import combinations, groupby


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


def to_sorted_grid(points):
    points = sorted(points, key=lambda p: (p.y, p.x))
    result = []
    for _, group in groupby(points, key=lambda p: p.y):
        result.append(list(group))
    return result


@dataclass
class CompressedPoint:
    x: int
    y: int
    true_x: int
    true_y: int

    @staticmethod
    def of_point(p, x, y):
        return CompressedPoint(x=x, y=y, true_x=p.x, true_y=p.y)


def compress(points):
    all_x = set()
    for row in points:
        for p in row:
            all_x.add(p.x)
    sorted_unique_x = sorted(list(all_x))
    x_map = {val: i for i, val in enumerate(sorted_unique_x)}

    compressed = []
    y = 0
    for row in points:
        r = []
        for p in row:
            x = x_map[p.x]
            r.append(CompressedPoint.of_point(p, x, y))
        compressed.append(r)
        y += 1
    print(compressed)
    return compressed

def print_map(points):
    max_x = 0
    max_y = 0
    for row in points:
        for p in row:
            if p.x > max_x:
                max_x = p.x
            if p.y > max_y:
                max_y = p.y
    for y in range(max_y+1):
        for x in range(max_x+1):
            point = False
            for row in points:
                for p in row:
                    if (x == p.x and y == p.y):
                        print("#", end="")
                        point = True
                        break
            if point:
                continue
            print(".", end="")
        print()


def task2(data):
    points = to_sorted_grid(data)
    compressed = compress(points)
    print_map(compressed)


app = AdventDay()
app.run(test=True)
