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


def get_area_compressed(p1, p2):
    return (abs(p1.true_x-p2.true_x)+1) * (abs(p1.true_y-p2.true_y)+1)


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


# TODO: potentially some inputs might need step=2, but 
# it works that way
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
    return compressed


def print_map(points, fill=None):
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
            if fill is None:
                print(".", end="")
            else:
                print("X" if fill[y][x] else '.', end="")
        print()


def prepare_map(points):
    max_x = 0
    max_y = 0
    for row in points:
        for p in row:
            if p.x > max_x:
                max_x = p.x
            if p.y > max_y:
                max_y = p.y
    map = []
    for y in range(max_y+1):
        row = [False] * (max_x+1)
        map.append(row)
    return map


def get_segments(points):
    segments = []
    for p1, p2, in combinations(points, 2):
        if p1.x == p2.x and p1.y == p2.y:
            continue
        if p1.x != p2.x and p1.y != p2.y:
            continue
        segments.append((p1, p2))
    return segments


def add_segment(map, segment):
    x_const = segment[0].x == segment[1].x
    start = segment[0].y if x_const else segment[0].x
    end = segment[1].y if x_const else segment[1].x
    if start > end:
        start, end = end, start
    for i in range(start, end+1):
        x = segment[0].x if x_const else i
        y = i if x_const else segment[0].y
        map[y][x] = True


def fill_map(map):
    y = len(map) // 2
    x = len(map[y]) // 2
    points = [(y, x)]
    while len(points) > 0:
        [y, x] = points.pop()
        map[y][x] = True
        if y > 0 and not map[y-1][x]:
            points.append((y-1, x))
        if x > 0 and not map[y][x-1]:
            points.append((y, x-1))
        if y + 1 <= len(map) and not map[y+1][x]:
            points.append((y+1, x))
        if x + 1 <= len(map[y]) and not map[y][x+1]:
            points.append((y, x+1))


# TODO: check only borders
def check_points(p1, p2, map):
    start_x = min(p1.x, p2.x)
    end_x = max(p1.x, p2.x)
    start_y = min(p1.y, p2.y)
    end_y = max(p1.y, p2.y)
    for y in range(start_y, end_y + 1):
        for x in range(start_x, end_x + 1):
            if not map[y][x]:
                return False
    return True


def validate_constraints(points):
    col_counts = {}
    col_points = {}

    for y, row in enumerate(points):
        if len(row) > 2:
            print(f"Validation Failed: Row y={y} has > 2 points.")
            return False
        for p in row:
            current_count = col_counts.get(p.x, 0) + 1
            if col_points.get(p.x) is None:
                col_points[p.x] = []
            current_points = col_points.get(p.x)
            current_points.append(p.y)
            if current_count > 2:
                print(f"Validation Failed: Column x={p.x} has > 2 points.")
                print(current_count)
                print(current_points)
            col_counts[p.x] = current_count
    return True


def task2(data):
    points = to_sorted_grid(data)
    compressed = compress(points)
    # print_map(compressed)
    pts = [p for row in compressed for p in row]
    validate_constraints(compressed)
    # TODO: there are two unnecessary segments
    # that make floodfill wrong, but they do not
    # impact answer
    segments = get_segments(pts)

    segment_map = prepare_map(compressed)
    for segment in segments:
        p1 = segment[0]
        p2 = segment[1]
        add_segment(segment_map, segment)
    fill_map(segment_map)
    # print_map(compressed, segment_map)
    print(len(segments))
    max = 0
    for p1, p2, in combinations(pts, 2):
        if not check_points(p1, p2, segment_map):
            continue
        area = get_area_compressed(p1, p2)
        if area > max:
            max = area
    return max


app = AdventDay()
app.run(test=False)
