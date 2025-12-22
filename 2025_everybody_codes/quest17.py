from utils.runner import AdventDay
from utils.loader import get_file
import heapq


def load(filename):
    data = get_file(filename)
    start = (0, 0)
    for i, row in enumerate(data):
        data[i] = [int(x) if x != '@' else 0 for x in row]
        if '@' in row:
            j = row.index('@')
            start = (i, j)
    return data, start


def check(start, point, r2):
    check = (start[0] - point[0])**2 + (start[1] - point[1])**2
    return check <= r2


def part1(data, start):
    r = 10
    r2 = r**2
    result = 0
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if check(start, (i, j), r2):
                result += val
    return result


def make_check_map(data, start):
    check_map = []
    for i, row in enumerate(data):
        check_row = []
        for j, val in enumerate(row):
            check = (start[0] - i)**2 + (start[1] - j)**2
            check_row.append(check)
        check_map.append(check_row)
    return check_map


def sum_for_step(data, check_map, step):
    r2 = step**2
    result = 0
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if check_map[i][j] <= r2:
                result += val
    return result


def part2(data, start):
    check_map = make_check_map(data, start)
    max_r = min(len(data), len(data[0])) // 2
    steps = [sum_for_step(data, check_map, i) for i in range(1, max_r+1)]
    steps = [y-x for x, y in zip([0] + steps, steps)]
    max_val, max_idx = max((val, idx+1) for idx, val in enumerate(steps))
    return max_val*max_idx


dirs = [
        (0, 1), (1, 0), (0, -1), (-1, 0)
]


def shortest_path_around(data, check_map, start, volcano, radius):
    heap = [(0, start, 0)]
    r2 = radius**2
    min_dist = {}
    time = (radius+1)*30
    while heap:
        distance, node, winding = heapq.heappop(heap)
        if node == start and winding != 0:
            return distance, node

        for dir in dirs:
            neighbor = (node[0]+dir[0], node[1]+dir[1])
            if neighbor[0] < 0 or neighbor[1] < 0:
                continue
            if neighbor[0] >= len(data) or neighbor[1] >= len(data[0]):
                continue
            if check_map[neighbor[0]][neighbor[1]] <= r2:
                continue
            cost = distance + data[neighbor[0]][neighbor[1]]
            if cost >= time:
                continue

            new_winding = winding
            if node[0] < volcano[0] and neighbor[0] < volcano[0]:
                if node[1] < volcano[1] and neighbor[1] >= volcano[1]:
                    new_winding += 1
                elif node[1] >= volcano[1] and neighbor[1] < volcano[1]:
                    new_winding -= 1
            if abs(new_winding) > 1:
                continue
            key = (neighbor, new_winding)

            if key in min_dist and min_dist[key] <= cost:
                continue
            min_dist[key] = cost
            heapq.heappush(
                    heap,
                    (cost, neighbor, new_winding)
            )
    return -1, None


def load3(filename):
    data = get_file(filename)
    start = (0, 0)
    volcano = (0, 0)
    for i, row in enumerate(data):
        data[i] = [int(x) if x not in ['@', 'S'] else 0 for x in row]
        if '@' in row:
            j = row.index('@')
            volcano = (i, j)
        if 'S' in row:
            j = row.index('S')
            start = (i, j)
    return data, volcano, start


app = AdventDay()


@app.test(592, file="data/day17/example3", desc="test 1")
@app.test(330, file="data/day17/e2", desc="test 2")
@app.test(3180, file="data/day17/e3", desc="test 3")
def part3(data, volcano, start):
    check_map = make_check_map(data, volcano)
    for i in range(1, 50):
        dist, node = shortest_path_around(data, check_map, start, volcano, i)
        if dist > 0:
            return dist*i


app.run()
